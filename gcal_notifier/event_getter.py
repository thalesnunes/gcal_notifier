from typing import Any, Dict, List
from .utils import CONFIG

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar


def make_conn(
    calendar: str = "primary", credentials: str = CONFIG + "/credentials.json"
) -> GoogleCalendar:

    return GoogleCalendar(calendar=calendar, credentials_path=credentials)


def load_calendars(
    general_params: Dict[str, Any], calendar_params: Dict[str, dict]
) -> Dict[str, GoogleCalendar]:

    calendars = {}
    for _, params in calendar_params.items():
        conn_params = {
                k: params[k] for k in params
                if k in ["calendar", "credentials"]
        }
        if "name" not in params:
            params["name"] = "Calendar"
        calendars[params["name"]] = make_conn(**conn_params).get_events(
            **general_params
        )
    return calendars


def load_events(calendars: List[GoogleCalendar]) -> List[Event]:

    events = []
    for name, calendar in calendars.items():
        for event in calendar:
            events.append(event)

    return events
