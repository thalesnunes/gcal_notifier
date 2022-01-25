import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from gcal_notifier.globals import CACHE


def load_events_file(
    path: Path = CACHE / "events_notify.json",
) -> List[Dict[str, Any]]:
    """Load cached events file.

    Args:
        path (Path): path to the events file

    Returns:
        List[Dict[str, Any]]: List of events as dictionaries
    """

    with open(path, "r") as json_file:
        json_events = json.load(json_file)

    return json_events


def str_to_datetime(date_str: str) -> datetime:
    """String to datetime.

    Args:
        date_str (str): date_str

    Returns:
        datetime: Datetime object
    """
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S%z")


def load_saved_events(
    path: Path = CACHE / "events_notify.json",
) -> List[Dict[str, Any]]:
    """Load events file and transforma datetime strings into datetime objects.

    Returns:
        List[Dict[str, Any]]: List of events as dictionaries
    """

    json_events = load_events_file(path)
    for event in json_events:
        for att in ["start", "end"]:
            event[att] = str_to_datetime(event[att])

    return json_events
