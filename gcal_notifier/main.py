#!/usr/bin/env python
from gcal_notifier.cli import cli
from gcal_notifier.config_reader import init_config
from gcal_notifier.event_getter import SimpleGCalendarGetter
from gcal_notifier.event_loader import load_saved_events
from gcal_notifier.event_reminder import SimpleGCalendarNotifier
from gcal_notifier.event_saver import save_events


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

    if args.command == "get":
        run_getter()
    else:
        run_notifier()
