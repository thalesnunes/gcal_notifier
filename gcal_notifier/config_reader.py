import os
from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, List, NoReturn, Tuple

from gcal_notifier.utils import CONFIG, GENERAL_PARAMS


def parse_int_list(input: str) -> List[int]:
    """Parse a list of ints from the config file.

    Args:
        input (str): Input list

    Returns:
        List[int]: List of ints
    """
    return list(int(value) for value in input.split(","))


def validate_config(config: ConfigParser) -> NoReturn:
    """Validate sections of config file.

    Args:
        config (ConfigParser): Config parser
    """
    for key in config.sections():
        if not (key == "GENERAL" or key.startswith("CALENDAR")):
            raise KeyError("Config section not valid")


def merge_general(config: ConfigParser) -> Dict[str, Any]:
    """Merge general configs with defaults.

    Args:
        config (ConfigParser): Config parser

    Returns:
        Dict[str, Any]: General params
    """
    return {
        **GENERAL_PARAMS,
        "single_events": config["GENERAL"].getboolean("single_events"),
        "order_by": config["GENERAL"].get("order_by"),
    }


def merge_calendars(config: ConfigParser) -> Dict[str, Any]:
    """Merge all calendars configs from config file.

    Args:
        config (ConfigParser): Config parser

    Returns:
        Dict[str, Any]: Dict with all the calendars' params
    """

    calendar_names = [
        calendar
        for calendar in config.sections()
        if calendar.startswith("CALENDAR")
    ]
    calendar_params = {}
    for calendar in calendar_names:
        cal = config[calendar]
        func_types = {
            "name": cal.get,
            "credentials": lambda k: os.path.expanduser(cal.get(k)),
            "calendar": cal.get,
            "default_reminders": cal.getlist,
            "default_color": cal.get,
        }

        calendar_params[calendar] = {k: func_types[k](k) for k in cal}
    return calendar_params


def init_config(
    config_path: Path = CONFIG / "config.ini",
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Reads, validates and parses the config file.

    Args:
        config_path (Path): config_path. Defaults to CONFIG / "config.ini"

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: (General, Calendar)
    """

    config = ConfigParser(converters={"list": parse_int_list})
    config.read(config_path)
    validate_config(config)
    general_params = merge_general(config)
    calendar_params = merge_calendars(config)
    return general_params, calendar_params
