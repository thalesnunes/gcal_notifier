from datetime import datetime
import json
from pathlib import Path
from typing import Any, List, Dict


def load_events_file(path: str = '/tmp/events.json') -> List[Dict[str, Any]]:

    with open(Path(path), 'r') as json_file:
        json_events = json.load(json_file)

    return json_events


def str_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str)


def load_saved_events() -> List[Dict[str, Any]]:

    json_events = load_events_file()
    for event in json_events:
        for att in ['start', 'end']:
            event[att] = str_to_datetime(event[att])

    return json_events
