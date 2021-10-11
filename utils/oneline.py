import json
import os
import shutil
import time
from .config import DIC_AGENTS, DIC_ENVS


class OneLine:
    def _path_check(self):
        if os.path.exists(self.dic_path["PATH_TO_WORK_DIRECTORY"]):
            if self.dic_path["PATH_TO_WORK_DIRECTORY"] != "records/default":
                raise FileExistsError
            else:
                pass
        else:
            os.makedirs(self.dic_path["PATH_TO_WORK_DIRECTORY"])

        if os.path.exists(self.dic_path["PATH_TO_MODEL"]):
            if self.dic_path["PATH_TO_MODEL"] != "model/default":
                raise FileExistsError
            else:
                pass
        else:
            os.makedirs(self.dic_path["PATH_TO_MODEL"])
    def _copy_conf_file(self, path=None):
        if path is None:
            path = self.dic_path["PATH_TO_WORK_DIRECTORY"]
        json.dump(self.dic_agent_conf, open(os.path.join(path, "agent.conf"), "w"),
                  indent=4)
        json.dump(self.dic_traffic_env_conf,
                  open(os.path.join(path, "traffic_env.conf"), "w"), indent=4)

    def _copy_anon_file(self, path=None):
        if path is None:
            path = self.dic_path["PATH_TO_WORK_DIRECTORY"]
        shutil.copy(os.path.join(self.dic_path["PATH_TO_DATA"], self.dic_traffic_env_conf["TRAFFIC_FILE"]),
                    os.path.join(path, self.dic_traffic_env_conf["TRAFFIC_FILE"]))
        shutil.copy(os.path.join(self.dic_path["PATH_TO_DATA"], self.dic_traffic_env_conf["ROADNET_FILE"]),
                    os.path.join(path, self.dic_traffic_env_conf["ROADNET_FILE"]))

    def __init__(self, dic_agent_conf, dic_traffic_env_conf, dic_path):
        self.dic_agent_conf = dic_agent_conf
        self.dic_traffic_env_conf = dic_traffic_env_conf
        self.dic_path = dic_path
        self.agents = []

        self._path_check()
        self._copy_conf_file()
        assert self.dic_traffic_env_conf["SIMULATOR_TYPE"] == 'anon'
        self._copy_anon_file()

        for i in range(dic_traffic_env_conf['NUM_INTERSECTIONS']):
            agent_name = self.dic_traffic_env_conf["MODEL_NAME"]
            agent = DIC_AGENTS[agent_name](
                dic_agent_conf=dic_agent_conf,
                dic_traffic_env_conf=dic_traffic_env_conf,
                dic_path=dic_path,
                cnt_round=0,
                intersection_id=str(i)
            )
            self.agents.append(agent)

        self.env = DIC_ENVS[self.dic_traffic_env_conf["SIMULATOR_TYPE"]](
                           path_to_log=self.dic_path["PATH_TO_WORK_DIRECTORY"],
                           path_to_work_directory=self.dic_path["PATH_TO_WORK_DIRECTORY"],
                           dic_traffic_env_conf=self.dic_traffic_env_conf)

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
            memory_str = 'time = {0}\taction = {1}\tcurrent_phase = {2}\treward = {3}'.format(current_time,
                          str(action_list), str([state[i]["cur_phase"][0] for i in range(len(state))]), str(reward),)
            f_memory.write(memory_str + "\n")
            f_memory.close()
            current_time = self.env.get_current_time()  # in seconds

            state = next_state
            step_num += 1

        print("Training time: ", time.time()-start_time)

        self.env.batch_log_2()
