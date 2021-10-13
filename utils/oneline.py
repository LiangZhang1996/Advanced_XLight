from .config import DIC_AGENTS
from .cityflow_env import CityFlowEnv
from .pipeline import path_check, copy_cityflow_file, copy_conf_file
import os
import time


class OneLine:

    def __init__(self, dic_agent_conf, dic_traffic_env_conf, dic_path):
        self.dic_agent_conf = dic_agent_conf
        self.dic_traffic_env_conf = dic_traffic_env_conf
        self.dic_path = dic_path
        self.agents = []
        self.env = None
        self.initialize()

    def initialize(self):
        path_check(self.dic_path)
        copy_conf_file(self.dic_path, self.dic_agent_conf, self.dic_traffic_env_conf)
        copy_cityflow_file(self.dic_path, self.dic_traffic_env_conf)

        for i in range(self.dic_traffic_env_conf['NUM_INTERSECTIONS']):
            agent_name = self.dic_traffic_env_conf["MODEL_NAME"]
            agent = DIC_AGENTS[agent_name](
                dic_agent_conf=self.dic_agent_conf,
                dic_traffic_env_conf=self.dic_traffic_env_conf,
                dic_path=self.dic_path,
                cnt_round=0,
                intersection_id=str(i)
            )
            self.agents.append(agent)
        self.env = CityFlowEnv(
            path_to_log=self.dic_path["PATH_TO_WORK_DIRECTORY"],
            path_to_work_directory=self.dic_path["PATH_TO_WORK_DIRECTORY"],
            dic_traffic_env_conf=self.dic_traffic_env_conf
        )

    def train(self):
        print("================ start train ================")
        total_run_cnt = self.dic_traffic_env_conf["RUN_COUNTS"]
        # initialize output streams
        file_name_memory = os.path.join(self.dic_path["PATH_TO_WORK_DIRECTORY"], "memories.txt")
        done = False
        state = self.env.reset()
        step_num = 0
        print("end reset")
        current_time = self.env.get_current_time()  # in seconds

        start_time = time.time()
        while not done and current_time < total_run_cnt:
            action_list = []

            for i in range(len(state)):
                one_state = state[i]
                count = step_num
                action = self.agents[i].choose_action(count, one_state)
                action_list.append(action)
            next_state, reward, done, _ = self.env.step(action_list)
            f_memory = open(file_name_memory, "a")
            # output to std out and file
            memory_str = 'time = {0}\taction = {1}\tcurrent_phase = {2}\treward = {3}'.\
                format(current_time, str(action_list), str([state[i]["cur_phase"][0] for i in range(len(state))]),
                       str(reward),)
            f_memory.write(memory_str + "\n")
            f_memory.close()
            current_time = self.env.get_current_time()  # in seconds

            state = next_state
            step_num += 1

        print("Training time: ", time.time()-start_time)

        self.env.batch_log_2()
