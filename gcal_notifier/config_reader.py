from configparser import ConfigParser
from .utils import CONFIG

def init_config(config_path: str = CONFIG+'/config.ini'):
    config = ConfigParser()
    config.read(config_path)
    return config

