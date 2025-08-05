from datetime import datetime, timedelta
from typing import Any, Dict, List

from gcal_notifier.globals import CMD
from gcal_notifier.utils import run_notify


class SimpleGCalendarNotifier:
    """Notifier for GoogleCalendar events.

    Args:
        events (List[Dict[str, Any]]): List of all cached events
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params

    Attributes:
        events (List[Dict[str, Any]]): List of all events
    """

    events: List[Dict[str, Any]]

    def __init__(
        self,
        events: List[Dict[str, Any]],
        general_params: Dict[str, Any],
        calendar_params: Dict[str, Any],
    ) -> None:

        self.events = events
        self.general_params = general_params

    def search_reminders(self) -> None:
        """Search current reminders to notify."""
        now = datetime.now().astimezone()
        for event in self.events:
            start = event["start"]
            if now > start + timedelta(minutes=1):
                continue
            for reminder in event["reminders"]:
                if now < start - timedelta(minutes=reminder):
                    continue
                elif now >= start - timedelta(
                    minutes=reminder
                ) and now < start - timedelta(minutes=reminder - 1):
                    cmd = self.create_command(event, event.get("cmd", CMD))
                    run_notify(
                        cmd,
                        self.general_params["notification_sound"],
                        self.general_params["notification_sound_path"],
                    )

    @staticmethod
    def create_command(event: Dict[str, Any], cmd: str = CMD) -> str:
        """Create a notify command formatting a cmd string.

        Args:
            event (Dict[str, Any]): Event info
            cmd (str): Base command to format
        """
        formatters = {
            "title": f'"{event.get("summary", None)}"',
            "calendar": f'"{event.get("calendar", None)}"',
            "start": f'"{event.get("start", None).strftime("%H:%M")}"',
            "end": f'"{event.get("end", None).strftime("%H:%M")}"',
            "description": f'"{event.get("description", None)}"',
            "link": f'"{event.get("other").get("hangoutLink", None)}"',
        }
        if not formatters["link"]:
            formatters["link"] = formatters["description"]

        return cmd.format(**formatters)
