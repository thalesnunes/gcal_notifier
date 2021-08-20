import os
from typing import Tuple
from configparser import ConfigParser

from .utils import CONFIG, GENERAL_PARAMS


def parse_int_list(input: str) -> list:
    return list(int(value) for value in input.split(","))


def validate_config(config: ConfigParser):

    for key in config.sections():
        if not (key == "GENERAL" or key.startswith("CALENDAR")):
            raise KeyError("Config section not valid")


def merge_general(config: ConfigParser) -> dict:

    params = {
        **GENERAL_PARAMS,
        "single_events": config["GENERAL"].getboolean("single_events"),
        "order_by": config["GENERAL"].get("order_by"),
    }
    return params


def merge_calendars(config: ConfigParser) -> dict:

    calendar_names = [
        calendar for calendar in config.sections()
        if calendar.startswith("CALENDAR")
    ]
    calendar_params = {}
    for calendar in calendar_names:
        cal = config[calendar]
        func_types = {
            "name": cal.get,
            "credentials": lambda k: os.path.expanduser(cal.get(k)),
            "calendar": cal.get,
            "default_reminder": cal.getlist,
        }

        calendar_params[calendar] = {k: func_types[k](k) for k in cal}
    return calendar_params


def init_config(
    config_path: str = CONFIG + "/config.ini",
) -> Tuple[ConfigParser, dict, dict]:

    config = ConfigParser(converters={"list": parse_int_list})
    config.read(config_path)
    validate_config(config)
    general_params = merge_general(config)
    calendar_params = merge_calendars(config)
    return config, general_params, calendar_params
