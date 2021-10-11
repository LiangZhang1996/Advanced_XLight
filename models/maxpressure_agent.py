from .agent import Agent
import numpy as np


class MaxPressureAgent(Agent):

    def __init__(self, dic_agent_conf, dic_traffic_env_conf, dic_path, cnt_round, intersection_id):

        super(MaxPressureAgent, self).__init__(dic_agent_conf, dic_traffic_env_conf, dic_path, intersection_id)

        self.current_phase_time = 0
        self.phase_length = len(self.dic_traffic_env_conf["PHASE"][self.dic_traffic_env_conf["SIMULATOR_TYPE"]])

        self.action = None

        self.DIC_PHASE_MAP = {
                1: 0,
                2: 1,
                3: 2,
                4: 3,
                0: 0
        }

    def choose_action(self, count, state):
        """
        As described by the definition, use traffic_movement_pressure
        to calcualte the pressure of each phase.
        """
        if state["cur_phase"][0] == -1:
            return self.action

        cur_phase = self.DIC_PHASE_MAP[state["cur_phase"][0]]
        #  WT_ET
        tr_mo_pr = np.array(state["traffic_movement_pressure_queue"])
        phase_1 = tr_mo_pr[1] + tr_mo_pr[4]
        # NT_ST
        phase_2 = tr_mo_pr[7] + tr_mo_pr[10]
        # WL_EL
        phase_3 = tr_mo_pr[0] + tr_mo_pr[3]
        # NL_SL
        phase_4 = tr_mo_pr[6] + tr_mo_pr[9]

        self.action = np.argmax([phase_1, phase_2, phase_3, phase_4])

        if state["cur_phase"][0] == self.action:
            self.current_phase_time += 1
        else:
            self.current_phase_time = 0

        return self.action
