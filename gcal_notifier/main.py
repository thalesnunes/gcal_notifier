from .config_reader import init_config
from .event_getter import load_calendars, load_events
from .event_loader import load_saved_events
from .event_reminder import *
from .event_saver import save_events


class SimpleGCalendarGetter:

    def __init__(self):
        self.config, self.general_params, self.calendar_params = init_config()
        self.calendars = load_calendars(
                self.general_params,
                self.calendar_params
            )
        self.events = load_events(self.calendars)
        save_events(self.events)


class SimpleGCalendarNotifier:

    def __init__(self):
        self.events = load_saved_events()
        print(self.events)
