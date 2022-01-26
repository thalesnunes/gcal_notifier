import os
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Tuple

from gcal_notifier.globals import COLORS, GCAL_COLORS
from gcal_notifier.tabulate import tabulate


class SimpleGCalendarPrinter:
    """Printer for calendar events.

    Args:
        events (List[Dict[str, Any]]): List of events
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
        period (Tuple[datetime, datetime]): (Start datetime, End datetime)
        use_color (bool): Use colors in output
        art_style (str): Style of output

    Attributes:
        events (List[Dict[str, Any]]): List of events
        use_color (bool): Use colors in output
        art_style (str): Style of output
        time_min (datetime): Lower bound of time interval
        time_max (datetime): Upper bound of time interval
    """

    events: List[Dict[str, Any]]
    use_color: bool
    art_style: str
    time_min: datetime
    time_max: datetime
    agenda: Dict[date, List[Dict[str, Any]]]
    fmt_cal: Dict[str, List[str]]

    def __init__(
        self,
        events: List[Dict[str, Any]],
        general_params: Dict[str, Any],
        calendar_params: Dict[str, Any],
        period: Tuple[datetime, datetime],
        use_color: bool = True,
        art_style: str = "fancy_grid",
        format: str = "day",
    ) -> None:
        """__init__.

        Args:
            events (List[Dict[str, Any]]): events
            general_params (Dict[str, Any]): general_params
            calendar_params (Dict[str, Any]): calendar_params
            period (Tuple[datetime, datetime]): period
            use_color (bool): use_color
            art_style (str): art_style
            format (str): format

        Returns:
            None:
        """

        self.events = events

        self.general_params = general_params
        self.calendar_params = calendar_params

        self.use_color = use_color
        self.art_style = art_style

        self.time_min, self.time_max = period

        self.prep_agenda()

    @staticmethod
    def get_colorcode(colorname: str) -> str:
        """Get colorcode with colorname.

        Args:
            colorname (str): Color name

        Returns:
            str: Color code of color name
        """
        return COLORS.get(colorname, "")

    def create_msg(self, msg: str, colorname: str = "default") -> str:
        """Print message given with given color.

        Args:
            msg (str): Message
            colorname (str): Color name

        Returns:
            str: Message formated with color, if self.use_color is True
        """
        if self.use_color:
            msg = (
                self.get_colorcode(colorname)
                + msg
                + self.get_colorcode("default")
            )
        return msg

    def get_text_from_event(self, event: Dict[str, Any]) -> str:
        """Format a colored text output from event.

        Args:
            event (Dict[str, Any]): Event

        Returns:
            str: Formatted and colored text
        """

        if event["end"] - event["start"] < timedelta(days=1):
            display_txt = (
                f'{event["start"].strftime("%H:%M")} - {event["summary"]}'
            )
        else:
            display_txt = event["summary"]

        default_color = self.calendar_params[event["cal_code"]].get(
            "default_color", "default"
        )
        event_color = GCAL_COLORS.get(event["color_id"], default_color)
        colored = self.create_msg(display_txt, event_color)

        return colored

    def prep_agenda(self) -> None:
        """Prepares the agenda to add the events later."""
        self.agenda = {
            (self.time_min + timedelta(days=i)).date(): []
            for i in range((self.time_max - self.time_min).days + 1)
        }

    def add_events_agenda(self, events: List[Dict[str, Any]]) -> None:
        """Add events to the weekly agenda in the string format.

        Args:
            events (List[Dict[str, Any]]): List of events
        """
        for event in events:
            duration = event["end"] - event["start"] - timedelta(seconds=1)
            for to_add in range(duration.days + 1):
                event_date = event["start"].date() + timedelta(days=to_add)
                if event_date in self.agenda:
                    self.agenda[event_date].append(event)

    def create_formatted_calendar(self) -> None:
        """Creates the formatted calendar for "week" and "month" formats.
        """

        self.fmt_cal = {}
        for day, events in self.agenda.items():
            weekday = day.strftime("%A")
            if weekday not in self.fmt_cal:
                if day.day == 1 and weekday != "Sunday":
                    start_of_week = day - timedelta(days=day.weekday() + 1)
                    while start_of_week.strftime("%A") != weekday:
                        self.fmt_cal[start_of_week.strftime("%A")] = [""]
                        start_of_week += timedelta(days=1)
                self.fmt_cal[weekday] = []

            self.fmt_cal[weekday].append(
                self.create_msg(day.strftime("%d"), "brightwhite")
            )
            for event in events:
                self.fmt_cal[weekday][-1] += "\n" + self.get_text_from_event(
                    event
                )

        self.fill_event_matrix()

    def fill_event_matrix(self, fill_value: str = "") -> None:
        """Fill the matrix with a fill_value so it is symmetrical.

        Args:
            fill_value (str): Value to be used to fill the lists.
        """
        max_len = max(map(len, self.fmt_cal.values()))
        if max_len == 0:
            self.fmt_cal = {key: [fill_value] for key in self.fmt_cal.keys()}
        else:
            for day, events in self.fmt_cal.items():
                self.fmt_cal[day] += [fill_value] * (max_len - len(events))

    def print_events(self, format: str = "day") -> None:
        """Prints the events using the given format.

        Args:
            format (str): Format used to print the events
        """

        self.add_events_agenda(self.events)

        if format.startswith("d"):
            for day, events in self.agenda.items():
                if len(events) > 0:
                    print()
                    print(
                        self.create_msg(
                            day.strftime("%d/%m - %A:"), "brightwhite"
                        )
                    )
                    for event in events:
                        print(" ", self.get_text_from_event(event))
        else:
            self.create_formatted_calendar()

            vert_size = os.get_terminal_size().columns

            output_events = tabulate(
                self.fmt_cal,
                headers="keys",
                tablefmt=self.art_style,
                maxcolwidths=vert_size // 7 - 3,
                disable_numparse=True,
            )
            print(output_events)
