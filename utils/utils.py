from .pipeline import Pipeline
from .oneline import OneLine
from . import config
import os
import json
import shutil
import copy


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
    oneline = OneLine(dic_agent_conf=dic_agent_conf,
                      dic_traffic_env_conf=merge(config.dic_traffic_env_conf, dic_traffic_env_conf),
                      dic_path=merge(config.DIC_PATH, dic_path)
                      )
    oneline.train()
    return

