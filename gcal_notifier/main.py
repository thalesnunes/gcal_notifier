from .config_reader import init_config
from .event_getter import load_calendars
from .event_reminder import *


class SimpleGCalendarNotifier:
    def __init__(self):

        self.config, self.general_params, self.calendar_params = init_config()
        self.calendars = load_calendars(
                self.general_params,
                self.calendar_params
            )
        self.show_calendar_params()
        self.show_events()

    def show_calendar_params(self):
        print(self.calendar_params)

    def show_events(self):
        for name, calendar in self.calendars.items():
            print(name)
            for event in calendar:
                print(event)
