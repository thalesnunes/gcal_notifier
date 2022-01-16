import json
import os
from datetime import datetime, time
from pathlib import Path
from typing import Any, Dict, List, NoReturn

from gcsa.event import Event

from gcal_notifier.utils import CONFIG

TZINFO = datetime.utcnow().astimezone().tzinfo


def event_to_dict(event: Event) -> Dict[str, Any]:
    """Transform instance of Event to Dict.

    Args:
        event (Event): Event

    Returns:
        Dict[str, Any]: Dict with the attributes of Event
    """
    return event.__dict__


def events_to_json(events: List[Event]) -> List[Dict[str, Any]]:
    """Transforms list of Events to list of dicts.

    Args:
        events (List[Event]): List of Events

    Returns:
        List[Dict[str, Any]]: List of Dicts with the Events attributes
    """
    return list(map(event_to_dict, events))


def date_to_datetime(date_obj: Any) -> Any:
    """Transforms date to datetime.

    Args:
        date_obj (date): Date object

    Returns:
        datetime: Datetime object
    """
    return datetime.combine(date_obj, time(tzinfo=TZINFO))


def event_sorter(event: Dict[str, Any]) -> Any:
    """Returns start date as datetime for sorting.

    Args:
        event (Dict[str, Any]): Event

    Returns:
        datetime: Start time as datetime object
    """
    start = event.get("start")
    if not isinstance(start, datetime):
        event["start"] = date_to_datetime(start)
        event["end"] = date_to_datetime(event.get("end"))
    return event.get("start")


def transform_events(events: List[Event]) -> List[Dict[str, Any]]:
    """Transform list of events to a sorted list of dicts.

    Args:
        events (List[Event]): List of events

    Returns:
        List[Dict[str, Any]]: List of sorted dict events
    """

    json_events = events_to_json(events)
    json_events.sort(key=event_sorter)
    return json_events


def save_events(
    events: List[Event], file_path: Path = CONFIG / "tmp" / "events.json"
) -> NoReturn:
    """Save events to a cache file.

    Args:
        events (List[Event]): List of Events
        file_path (str): Path to file to be saved
    """

    json_events = transform_events(events)

    file_path = Path(file_path)
    os.makedirs(file_path.parent, exist_ok=True)
    with open(Path(file_path), "w") as json_out:
        json.dump(
            json_events,
            json_out,
            ensure_ascii=False,
            indent=4,
            cls=DatetimeEncoder,
        )


class DatetimeEncoder(json.JSONEncoder):
    """Encoder for datetime objects."""

    def default(self, o: Any) -> str:
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            if isinstance(o, datetime):
                return o.strftime("%Y-%m-%d %H:%M:%S%z")
            return str(o)
