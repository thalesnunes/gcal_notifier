from .cli import cli
from .config_reader import init_config
from .event_getter import SimpleGCalendarGetter
from .event_loader import load_saved_events
from .event_reminder import SimpleGCalendarNotifier
from .event_saver import save_events


def run_getter():
    general_params, calendar_params = init_config()
    getter = SimpleGCalendarGetter(general_params, calendar_params)
    save_events(getter.events)


def run_notifier():
    general_params, calendar_params = init_config()
    saved_events = load_saved_events()
    SimpleGCalendarNotifier(saved_events, general_params, calendar_params)


def gcal_notifier():

    args = cli()

    if args.command == 'get':
        run_getter()
    else:
        run_notifier()
