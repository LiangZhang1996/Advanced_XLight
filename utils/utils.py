import copy
from .pipeline import Pipeline
from .oneline import OneLine
from . import config


def memo_rename(traffic_file_list):
    new_name = ""
    for traffic_file in traffic_file_list:
        if "synthetic" in traffic_file:
            sta = traffic_file.rfind("-") + 1
            print(traffic_file, int(traffic_file[sta:-4]))
            new_name = new_name + "syn" + traffic_file[sta:-4] + "_"
        elif "cross" in traffic_file:
            sta = traffic_file.find("equal_") + len("equal_")
            end = traffic_file.find(".xml")
            new_name = new_name + "uniform" + traffic_file[sta:end] + "_"
        elif "flow" in traffic_file:
            new_name = traffic_file[:-4]
    new_name = new_name[:-1]
    return new_name


def merge(dic_tmp, dic_to_change):
    dic_result = copy.deepcopy(dic_tmp)
    dic_result.update(dic_to_change)
    return dic_result


def pipeline_wrapper(dic_agent_conf, dic_traffic_env_conf, dic_path):
    ppl = Pipeline(dic_agent_conf=dic_agent_conf,
                   dic_traffic_env_conf=dic_traffic_env_conf,
                   dic_path=dic_path
                   )
    ppl.run(multi_process=False)

    print("pipeline_wrapper end")
    return


def oneline_wrapper(dic_agent_conf, dic_traffic_env_conf, dic_path):
    oneline = OneLine(dic_agent_conf=merge(getattr(config, "DIC_{0}_AGENT_CONF".
                                                   format(dic_traffic_env_conf["MODEL_NAME"].upper())),
                                           dic_agent_conf),
                      dic_traffic_env_conf=merge(config.dic_traffic_env_conf, dic_traffic_env_conf),
                      dic_path=merge(config.DIC_PATH, dic_path)
                      )
    oneline.train()
    return


