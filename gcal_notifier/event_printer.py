from tabulate import tabulate
from typing import Any, Dict, List, NoReturn
import sys

from gcal_notifier.utils import ART_CHARS, COLORS


class SimpleGCalendarPrinter:

    def __init__(
        self,
        events: List[Dict[str, Any]],
        general_params: Dict[str, Any],
        calendar_params: Dict[str, Any],
        use_color: bool = True,
        art_style: str = 'fancy',
    ) -> NoReturn:

        self.colors = COLORS
        self.use_color = use_color
        self.colorset = set(self.colors.keys())

        self.art_style = art_style
        self.art = ART_CHARS[self.art_style]

    def get_colorcode(self, colorname: str) -> str:
        return self.colors.get(colorname, '')

    def msg(
            self, msg: str, colorname: str = 'default', file: Any = sys.stdout
    ) -> NoReturn:
        if self.use_color:
            msg = self.colors[colorname] + msg + self.colors['default']
        file.write(msg)

    def err_msg(self, msg: str) -> NoReturn:
        self.msg(msg, 'brightred', file=sys.stderr)

    def debug_msg(self, msg: str) -> NoReturn:
        self.msg(msg, 'yellow', file=sys.stderr)

    def art_msg(
            self, arttag: str, colorname: str, file: Any = sys.stdout
    ) -> NoReturn:
        self.msg(self.art[arttag], colorname, file=file)
