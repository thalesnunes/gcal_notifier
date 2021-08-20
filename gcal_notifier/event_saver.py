import json
import os
from pathlib import Path
from typing import Dict, List

from gcsa.event import Event


def event_to_dict(event: Event):
    return event.__dict__


def events_to_json(events: List[Event]) -> List[Dict]:
    return list(map(event_to_dict, events))


def save_events(events: List[Event], file_path: str = './tmp/events.json'):

    json_events = events_to_json(events)
    json_events.sort(key=lambda event: event.get('start'))

    file_path = Path(file_path)
    os.makedirs(file_path.parent, exist_ok=True)
    with open(Path(file_path), 'w') as json_out:
        json.dump(
                json_events,
                json_out,
                ensure_ascii=False,
                indent=4,
                cls=DatetimeEncoder
        )


class DatetimeEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)
