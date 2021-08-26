from datetime import datetime, date, time
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from gcsa.event import Event

from gcal_notifier.utils import CONFIG


def event_to_dict(event: Event) -> Dict[str, Any]:
    return event.__dict__


def events_to_json(events: List[Event]) -> List[Dict[str, Any]]:
    return list(map(event_to_dict, events))


def date_to_datetime(date_obj: date) -> datetime:
    tzinfo = datetime.utcnow().astimezone().tzinfo
    return datetime.combine(date_obj, time(tzinfo=tzinfo))


def event_sorter(event: Dict[str, Any]) -> datetime:
    start = event.get("start")
    if not isinstance(start, datetime):
        event["start"] = date_to_datetime(start)
        event["end"] = date_to_datetime(event.get("end"))
    return event.get("start")


def transform_events(events: List[Event]) -> Dict[str, Any]:

    json_events = events_to_json(events)
    json_events.sort(key=event_sorter)
    return json_events


def save_events(
        events: List[Event], file_path: str = CONFIG / "tmp" / "events.json"
        ):

    json_events = transform_events(events)

    file_path = Path(file_path)
    os.makedirs(file_path.parent, exist_ok=True)
    with open(Path(file_path), "w") as json_out:
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
            if isinstance(o, datetime):
                return o.strftime("%Y-%m-%d %H:%M:%S%z")
            return str(o)
