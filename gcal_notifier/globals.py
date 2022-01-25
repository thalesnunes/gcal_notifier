from pathlib import Path

ROOT_DIR = Path(__file__).parent

CONFIG = Path("~/.config/gcal_notifier").expanduser()

CACHE = Path("~/.cache/gcal_notifier").expanduser()

GENERAL_PARAMS = {
    "order_by": "startTime",
    "single_events": True,
    "notification_sound": ROOT_DIR / "resources" / "pop.wav",
}

CMD = "notify-send -u critical -a GoogleCalendar {calendar} {title}"

COLORS = {
    "default": "\033[0m",
    "black": "\033[0;30m",
    "brightblack": "\033[30;1m",
    "red": "\033[0;31m",
    "brightred": "\033[31;1m",
    "green": "\033[0;32m",
    "brightgreen": "\033[32;1m",
    "yellow": "\033[0;33m",
    "brightyellow": "\033[33;1m",
    "blue": "\033[0;34m",
    "brightblue": "\033[34;1m",
    "magenta": "\033[0;35m",
    "brightmagenta": "\033[35;1m",
    "cyan": "\033[0;36m",
    "brightcyan": "\033[36;1m",
    "white": "\033[0;37m",
    "brightwhite": "\033[37;1m",
    None: "\033[0m",
}

GCAL_COLORS = {
    "1": "blue",
    "2": "brightgreen",
    "3": "brightblue",
    "4": "red",
    "5": "brightyellow",
    "6": "yellow",
    "7": "brightcyan",
    "8": "brightblack",
    "9": "cyan",
    "10": "green",
    "11": "brightred",
}
