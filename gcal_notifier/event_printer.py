import os
from typing import Any, Dict, List, NoReturn, Set

from gcal_notifier.globals import COLORS, GCAL_COLORS
from gcal_notifier.tabulate import tabulate


class SimpleGCalendarPrinter:
    """Printer for calendar events.

    Args:
        events (List[Dict[str, Any]]): List of events
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
        use_color (bool): Use colors in output
        art_style (str): Style of output

    Attributes:
        events: List[Dict[str, Any]]
        use_color (bool): Use colors in output
        colorset (Set[str]): Names of colors
        art_style (str): Style of output
        agenda (Dict[str, List[str]])
    """

    events: List[Dict[str, Any]]
    use_color: bool
    colorset: Set[str]
    art_style: str
    agenda: Dict[str, List[str]] = {
        "Sunday": [],
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
    }

    def __init__(
        self,
        events: List[Dict[str, Any]],
        general_params: Dict[str, Any],
        calendar_params: Dict[str, Any],
        use_color: bool = True,
        art_style: str = "fancy_grid",
    ) -> NoReturn:

        self.events = events

        self.general_params = general_params
        self.calendar_params = calendar_params

        self.use_color = use_color
        self.colorset = set(COLORS.keys())
        self.art_style = art_style

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

        display_txt = (
                f'{event["start"].strftime("%H:%M")} - {event["summary"]}'
            )
        default_color = self.calendar_params[event["cal_code"]].get(
                "default_color", "default"
            )
        event_color = GCAL_COLORS.get(event["color_id"], default_color)
        colored = self.create_msg(display_txt, event_color)

        return colored

    def add_events_agenda(self, events: List[Dict[str, Any]]) -> NoReturn:
        """Add events to the weekly agenda in the string format.

        Args:
            events (List[Dict[str, Any]]): List of events
        """
        for e in events:
            day_name = e["start"].strftime("%A")
            event_text = self.get_text_from_event(e)
            self.agenda[day_name].append(event_text)

    def fill_event_matrix(self, fill_value: str = "") -> NoReturn:
        """Fill the matrix with a fill_value so it is symmetrical.

        Args:
            fill_value (str): Value to be used to fill the lists.
        """

        max_len = max(map(len, self.agenda.values()))
        if max_len == 0:
            self.agenda = {key: [fill_value] for key in self.agenda.keys()}
        else:
            for day, events in self.agenda.items():
                self.agenda[day] += [fill_value] * (max_len - len(events))

    def print_events(self, format: str = "week") -> NoReturn:
        """Prints the events using the given format.

        Args:
            format (str): Format used to print the events
        """

        if format == "list" or format == "l":
            pass
        else:
            self.add_events_agenda(self.events)
            self.fill_event_matrix()

            vert_size = os.get_terminal_size().columns

            output_events = tabulate(
                self.agenda,
                headers="keys",
                tablefmt=self.art_style,
                maxcolwidths=vert_size // 7 - 2,
            )
        print(output_events)
