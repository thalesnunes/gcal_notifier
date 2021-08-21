from .utils import make_sound


class Reminder:

    def __init__(self):

        self.cmd = 'notify-send -u critical -a GCalendar {s} {b}'
