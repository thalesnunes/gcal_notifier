from .config_reader import init_config
from .event_getter import make_conn
from .event_scheduler import *
from .utils import DEFAULT_PARAMS

class SimpleGCalendarNotifier:

    def __init__(self):
        self.config = init_config()
        self.calendar = make_conn().get_events(**DEFAULT_PARAMS, **self.config['DEFAULT'])
        self.show_events()

    def show_events(self):
        for event in self.calendar:
            print(event)
