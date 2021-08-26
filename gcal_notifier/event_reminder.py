from datetime import datetime, timedelta
import shlex
import subprocess
from typing import Any, Dict, List

from gcal_notifier.utils import make_sound


class SimpleGCalendarNotifier:

    CMD: str = "notify-send -u critical -a GoogleCalendar {calendar} {title}"

    def __init__(
        self,
        events: List[Dict[str, Any]],
        general_params: Dict[str, Any],
        calendar_params: Dict[str, Any],
    ):
        self.events = events
        self.search_reminders()

    def search_reminders(self):
        now = datetime.now().astimezone()
        for event in self.events:
            start = event["start"]
            if now > start + timedelta(minutes=1):
                continue
            for reminder in event["reminders"]:
                if now < start - timedelta(minutes=reminder):
                    return
                elif now >= start - timedelta(
                    minutes=reminder
                ) and now < start - timedelta(minutes=reminder - 1):
                    cmd = self.create_command(event, event.get("cmd", self.CMD))
                    self.run_notify(cmd)

    @staticmethod
    def run_notify(command: str):
        subprocess.run(shlex.split(command))
        # TODO: implement configurable notification sound
        make_sound()

    @staticmethod
    def create_command(event: Dict[str, Any], cmd: str = CMD):
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
