from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, List
from gcal_notifier.utils import CONFIG, run_notify

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from google.auth.exceptions import RefreshError


class SimpleGCalendarGetter:
    config: ConfigParser
    general_params: Dict[str, Any]
    calendar_params: Dict[str, Any]
    calendars: Dict[str, GoogleCalendar]
    events: List[Dict[str, Event]]

    def __init__(
            self,
            general_params: Dict[str, Any],
            calendar_params: Dict[str, Any]
            ):
        self.general_params = general_params
        self.calendar_params = calendar_params
        self.load_calendars()
        self.load_events()

    def load_calendars(self):
        self.calendars = {}
        new_cal_params = {}
        for label, params in self.calendar_params.items():
            conn_params = {
                    k: params[k] for k in params
                    if k in ["calendar", "credentials"]
            }
            if "name" not in params:
                params["name"] = "Calendar"
            else:
                label = params["name"]
            self.calendars[params["name"]] = self.make_conn(
                                                name=params["name"],
                                                **conn_params
                                            ).get_events(**self.general_params)
            new_cal_params[label] = params
        self.calendar_params = new_cal_params

    def set_reminders(self, event: Event):
        if event.default_reminders:
            event_calendar = self.calendar_params[event.calendar]
            default_rem = event_calendar.get("default_reminders", [])
            event.reminders = sorted(default_rem, reverse=True)
        else:
            # TODO: implement when not default_reminders
            pass

    def load_events(self):
        self.events = []
        for name, calendar in self.calendars.items():
            for event in calendar:
                event.calendar = name
                self.set_reminders(event)
                self.events.append(event)

    @staticmethod
    def make_conn(
        name: str,
        calendar: str = "primary",
        credentials: Path = CONFIG / "default" / "credentials.json"
    ) -> GoogleCalendar:
        try:
            return GoogleCalendar(calendar=calendar, credentials_path=credentials)
        except RefreshError:
            (credentials.parent / "token.pickle").unlink()
            run_notify(f'notify-send -u critical -a GoogleCalendar {calendar} "You have to authorize the credentials inside {credentials} again!"')
            return GoogleCalendar(calendar=calendar, credentials_path=credentials)
