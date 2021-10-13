"""
EP-PressLight agent, based on LIT model structure.
Observations: [cur_phase, traffic_movement_pressure_queue_efficient]
Reward: -Pressure
"""
from .network_agent import NetworkAgent, Selector
from tensorflow.keras.layers import Dense, concatenate, Add, Multiply
from tensorflow.keras import Input, Model
from tensorflow.keras.optimizers import Adam
import numpy as np
import random


class EPressLightAgent(NetworkAgent):
    def build_network(self):
        dic_input_node = {"feat1": Input(shape=(8,), name="input_cur_phase"),
                          "feat2": Input(shape=(12,), name="input_feat2")}

        # concatenate features
        list_all_flatten_feature = []
        for feature_name in ["feat1", "feat2"]:
            list_all_flatten_feature.append(dic_input_node[feature_name])
        all_flatten_feature = concatenate(list_all_flatten_feature, axis=1, name="all_flatten_feature")

        # shared dense layer
        shared_dense = Dense(self.dic_agent_conf["D_DENSE"], activation="sigmoid",
                             name="shared_hidden")(all_flatten_feature)

        # build phase selector layer
        list_selected_q_values = []
        for phase_id in range(1, self.num_phases + 1):
            if self.dic_traffic_env_conf["BINARY_PHASE_EXPANSION"]:
                phase_expansion = self.dic_traffic_env_conf["PHASE"][phase_id]
            else:
                phase_expansion = phase_id
            locals()["q_values_{0}".format(phase_id)] = self._separate_network_structure(
                shared_dense, self.dic_agent_conf["D_DENSE"], self.num_actions, memo=phase_id)
            locals()["selector_{0}".format(phase_id)] = Selector(
                phase_expansion, d_phase_encoding=8, d_action=self.num_actions,
                name="selector_{0}".format(phase_id))(dic_input_node["feat1"])
            locals()["q_values_{0}_selected".format(phase_id)] = Multiply(name="multiply_{0}".format(phase_id))(
                [locals()["q_values_{0}".format(phase_id)],
                 locals()["selector_{0}".format(phase_id)]]
            )
            list_selected_q_values.append(locals()["q_values_{0}_selected".format(phase_id)])
        q_values = Add()(list_selected_q_values)

        network = Model(inputs=[dic_input_node[feature_name]
                                for feature_name in ["feat1", "feat2"]],
                        outputs=q_values)
        network.compile(optimizer=Adam(lr=self.dic_agent_conf["LEARNING_RATE"]),
                        loss="mean_squared_error")
        network.summary()

        return network

    @staticmethod
    def _separate_network_structure(state_features, dense_d, num_actions, memo=""):
        hidden_1 = Dense(dense_d, activation="relu", name="hidden_separate_branch_{0}_1".format(memo))(
            state_features)
        q_values = Dense(num_actions, activation="linear", name="q_values_separate_branch_{0}".format(memo))(hidden_1)
        return q_values

    def prepare_Xs_Y(self, memory):
        """
        designed for update simple dqn models
        """
        ind_end = len(memory)
        print("memory size before forget: {0}".format(ind_end))
        # use all the samples to pretrain, i.e., without forgetting

        ind_sta = max(0, ind_end - self.dic_agent_conf["MAX_MEMORY_LEN"])
        memory_after_forget = memory[ind_sta: ind_end]
        print("memory size after forget:", len(memory_after_forget))

        # sample the memory
        sample_size = min(self.dic_agent_conf["SAMPLE_SIZE"], len(memory_after_forget))
        sample_slice = random.sample(memory_after_forget, sample_size)
        print("memory samples number:", sample_size)

        # used_feature = ["phase_2", "phase_num_vehicle"]
        used_feature = self.dic_traffic_env_conf["LIST_STATE_FEATURE"][:2]
        _state = [[], []]
        _next_state = [[], []]
        _action = []
        _reward = []
        for i in range(len(sample_slice)):
            state, action, next_state, reward, _, _, _ = sample_slice[i]
            for feat_idx, feat_name in enumerate(used_feature):
                _state[feat_idx].append(state[feat_name])
                _next_state[feat_idx].append(next_state[feat_name])
            _action.append(action)
            _reward.append(reward)
        # well prepared states
        _state2 = [np.array(ss) for ss in _state]
        _next_state2 = [np.array(ss) for ss in _next_state]

        cur_qvalues = self.q_network.predict(_state2)
        next_qvalues = self.q_network_bar.predict(_next_state2)
        # [batch, 4]
        target = np.copy(cur_qvalues)

        for i in range(len(sample_slice)):
            target[i, _action[i]] = _reward[i] / self.dic_agent_conf["NORMAL_FACTOR"] + self.dic_agent_conf["GAMMA"] * \
                                    np.max(next_qvalues[i, :])
        self.Xs = _state2
        self.Y = target
