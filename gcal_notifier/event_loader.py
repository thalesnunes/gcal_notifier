from datetime import datetime
import json
from pathlib import Path
from typing import Any, List, Dict

from gcal_notifier.utils import CONFIG


def load_events_file(
    path: Path = CONFIG / "tmp" / "events.json",
) -> List[Dict[str, Any]]:

    with open(path, "r") as json_file:
        json_events = json.load(json_file)

    return json_events


def str_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S%z")


def load_saved_events() -> List[Dict[str, Any]]:

    json_events = load_events_file()
    for event in json_events:
        for att in ["start", "end"]:
            event[att] = str_to_datetime(event[att])

    return json_events
