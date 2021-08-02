from .config_reader import init_config
from .event_getter import load_calendars
from .event_scheduler import *

class SimpleGCalendarNotifier:

    def __init__(self):

        self.config, self.general_params, self.calendar_params = init_config()
        self.calendars = load_calendars(self.general_params, self.calendar_params)
        self.show_calendar_params()
        self.show_events()
        self.show_config()

    def show_calendar_params(self):
        print(self.calendar_params)

    def show_events(self):
        for name, calendar in self.calendars.items():
            print(name)
            for event in calendar:
                print(event)

    def show_config(self):
        print(self.config['CALENDAR1'].getlist('default_reminder'))
