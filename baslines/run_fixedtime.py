"""
Run the Fixed-Time model
On JiNan and HangZhou real data
"""
from utils.utils import oneline_wrapper
import os
import time
from multiprocessing import Process
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memo",       type=str,               default='benchmark_1001')
    parser.add_argument("-model",       type=str,               default="Fixedtime")
    parser.add_argument("-multi_process", action="store_true",  default=True)
    parser.add_argument("-workers",     type=int,               default=3)
    parser.add_argument("-hangzhou",    action="store_true",    default=False)
    parser.add_argument("-jinan",       action="store_true",    default=True)

    return parser.parse_args()


def main(in_args):
    if in_args.hangzhou:
        count = 3600
        road_net = "4_4"
        traffic_file_list = ["anon_4_4_hangzhou_real.json", "anon_4_4_hangzhou_real_5734.json",
                             "anon_4_4_hangzhou_real_5816.json"]
        template = "Hangzhou"
    elif in_args.jinan:
        count = 3600
        road_net = "3_4"
        traffic_file_list = ["anon_3_4_jinan_real.json", "anon_3_4_jinan_real_2000.json",
                             "anon_3_4_jinan_real_2500.json"]
        template = "Jinan"

    NUM_ROW = int(road_net.split('_')[0])
    NUM_COL = int(road_net.split('_')[1])
    num_intersections = NUM_ROW * NUM_COL
    print('num_intersections:', num_intersections)
    print(traffic_file_list)
    process_list = []
    for traffic_file in traffic_file_list:
        dic_traffic_env_conf_extra = {
            "NUM_AGENTS": num_intersections,
            "NUM_INTERSECTIONS": num_intersections,
            "MODEL_NAME": in_args.model,
            "RUN_COUNTS": count,
            "NUM_ROW": NUM_ROW,
            "NUM_COL": NUM_COL,
            "TRAFFIC_FILE": traffic_file,
            "ROADNET_FILE": "roadnet_{0}.json".format(road_net),
            "LIST_STATE_FEATURE": [
                "cur_phase",
                "time_this_phase",
                "traffic_movement_pressure_queue",
            ],
            "DIC_REWARD_INFO": {
                "pressure": 0
            },
        }

        dic_agent_conf_extra = {
            "FIXED_TIME": [15, 15, 15, 15],
        }

        dic_path_extra = {
            "PATH_TO_MODEL": os.path.join("model", in_args.memo, traffic_file + "_" +
                                          time.strftime('%m_%d_%H_%M_%S', time.localtime(time.time()))),
            "PATH_TO_WORK_DIRECTORY": os.path.join("records", in_args.memo, traffic_file + "_" +
                                                   time.strftime('%m_%d_%H_%M_%S', time.localtime(time.time()))),
            "PATH_TO_DATA": os.path.join("data", template, str(road_net))
        }
        if in_args.multi_process:
            process_list.append(Process(target=oneline_wrapper,
                                        args=(dic_agent_conf_extra,
                                              dic_traffic_env_conf_extra, dic_path_extra))
                                )
        else:
            oneline_wrapper(dic_agent_conf_extra, dic_traffic_env_conf_extra, dic_path_extra)

    if in_args.multi_process:
        list_cur_p = []
        for p in process_list:
            if len(list_cur_p) < in_args.workers:
                p.start()
                list_cur_p.append(p)
            if len(list_cur_p) < in_args.workers:
                continue

        for p in list_cur_p:
            p.join()


if __name__ == "__main__":
    args = parse_args()
    main(args)
