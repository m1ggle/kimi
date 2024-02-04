import yaml
import os

path = os.getcwd()


def read_config():
    """"读取配置"""
    with open(path + "/config/config.yaml") as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config
