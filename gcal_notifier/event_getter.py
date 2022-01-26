from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from google.auth.exceptions import RefreshError

from gcal_notifier.globals import CONFIG
from gcal_notifier.utils import run_notify


class SimpleGCalendarGetter:
    """Connector to fetch all events from multiple calendars.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params

    Attributes:
        config (ConfigParser): Config parser
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
        calendars (Dict[str, GoogleCalendar]): Calendar connections
        events (List[Dict[str, Event]]): List of all events
    """

    config: ConfigParser
    general_params: Dict[str, Any]
    calendar_params: Dict[str, Any]
    calendars: Dict[str, GoogleCalendar]
    events: List[Dict[str, Event]]

    def __init__(
        self,
        general_params: Dict[str, Any],
        calendar_params: Dict[str, Any],
    ) -> None:

        self.general_params = general_params
        self.calendar_params = calendar_params

    def load_calendars(self, period: Tuple[datetime, datetime]) -> None:
        """Load calendars from Google using the configs passed to the class.

        Args:
            period (Tuple[datetime, datetime]): (Start datetime, End datetime)
        """
        self.calendars = {}

        event_params = {
            k: v
            for k, v in self.general_params.items()
            if k in ["order_by", "single_events"]
        }
        event_params["time_min"], event_params["time_max"] = period

        for cal_code, params in self.calendar_params.items():
            conn_params = {
                k: params[k]
                for k in params
                if k in ["calendar", "credentials"]
            }
            self.calendars[cal_code] = self.make_conn(
                **conn_params
            ).get_events(**event_params)

    def set_reminders(self, event: Event) -> None:
        """Set reminders to event.

        Args:
            event (Event): event
        """
        if event.default_reminders:
            event_calendar = self.calendar_params[event.cal_code]
            new_reminders = event_calendar.get("default_reminders", [])
        else:
            new_reminders = []
            for reminder in event.reminders:
                if reminder.method == "popup":
                    new_reminders.append(reminder.minutes_before_start)

        event.reminders = sorted(new_reminders, reverse=True)

    def load_events(self) -> None:
        """Load event from fetched calendar."""
        self.events = []
        for cal_code, calendar in self.calendars.items():
            for event in calendar:
                event.cal_code = cal_code
                event.calendar = self.calendar_params[cal_code].get("name", "")
                self.set_reminders(event)
                self.events.append(event)

    @staticmethod
    def make_conn(
        calendar: str = "primary",
        credentials: Path = CONFIG / "default" / "credentials.json",
    ) -> GoogleCalendar:
        """Wrapper to connect to GoogleCalendar.

        Args:
            calendar (str): calendar
            credentials (Path): credentials

        Returns:
            GoogleCalendar: GoogleCalendar client
        """
        try:
            return GoogleCalendar(
                calendar=calendar, credentials_path=credentials
            )
        except RefreshError:
            (credentials.parent / "token.pickle").unlink()
            run_notify(
                f'notify-send -u critical -a GoogleCalendar {calendar} "You have to authorize the credentials inside {credentials} again!"'  # noqa
            )
            quit(1)
