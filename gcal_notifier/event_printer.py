import os
from typing import Any, Dict, List, NoReturn, Set

from gcal_notifier.tabulate import tabulate
from gcal_notifier.utils import COLORS, GCAL_COLORS


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
        art_style: str = "fancy",
    ) -> NoReturn:

        self.events = events

        self.general_params = general_params
        self.calendar_params = calendar_params

        self.use_color = use_color
        self.colorset = set(COLORS.keys())
        self.art_style = art_style

        self.add_events_agenda(self.events)

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

    def add_events_agenda(self, events: List[Dict[str, Any]]) -> NoReturn:
        """Add events to the weekly agenda in the string format.

        Args:
            events (List[Dict[str, Any]]): List of events
        """
        for e in events:
            day_name = e["start"].strftime("%A")
            display_txt = f'{e["start"].strftime("%H:%M")} - {e["summary"]}'
            default_color = self.calendar_params[e["cal_code"]].get(
                "default_color", "default"
            )
            event_color = GCAL_COLORS.get(e["color_id"], default_color)
            colored = self.create_msg(display_txt, event_color)
            self.agenda[day_name].append(colored)

        # Workaround to make word wraping work right
        max_len = max(map(len, self.agenda.values()))
        for day, events in self.agenda.items():
            self.agenda[day] += [""] * (max_len - len(events))

    def tabulate_events(self) -> NoReturn:
        """Tabulates and prints the events to the console."""
        vert_size = os.get_terminal_size().columns
        table = tabulate(
            self.agenda,
            headers="keys",
            tablefmt="fancy_grid",
            maxcolwidths=vert_size // 7 - 2,
        )
        print(table)
