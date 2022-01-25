#!/usr/bin/env python
from datetime import datetime
from typing import Any, Dict, NoReturn, Tuple

from gcal_notifier.cli import cli
from gcal_notifier.config_reader import init_config
from gcal_notifier.event_getter import SimpleGCalendarGetter
from gcal_notifier.event_loader import load_saved_events
from gcal_notifier.event_printer import SimpleGCalendarPrinter
from gcal_notifier.event_reminder import SimpleGCalendarNotifier
from gcal_notifier.event_saver import save_events, transform_events
from gcal_notifier.globals import CACHE
from gcal_notifier.utils import define_period


def run_getter(
    general_params: Dict[str, Any],
    calendar_params: Dict[str, Any],
    period: Tuple[datetime, datetime],
) -> NoReturn:
    """Run SimpleGCalendarGetter with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
        save_path (str): Path to file to be saved
    """
    getter = SimpleGCalendarGetter(general_params, calendar_params)
    getter.load_calendars(period)
    getter.load_events()
    save_events(getter.events, file_path=CACHE/"events_notify.json")


def run_notifier(
    general_params: Dict[str, Any], calendar_params: Dict[str, Any]
) -> NoReturn:
    """Run SimpleGCalendarNotifier with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
    """
    saved_events = load_saved_events()
    notifier = SimpleGCalendarNotifier(
        saved_events, general_params, calendar_params
    )
    notifier.search_reminders()


def run_printer(
    general_params: Dict[str, Any],
    calendar_params: Dict[str, Any],
    period: Tuple[datetime, datetime],
    format: str = "day"
) -> NoReturn:
    """Run SimpleGCalendarPrinter with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
        format (str): Format to use when printing events
    """
    getter = SimpleGCalendarGetter(general_params, calendar_params)
    getter.load_calendars(period)
    getter.load_events()
    events_to_print = transform_events(getter.events)
    printer = SimpleGCalendarPrinter(
        events_to_print, general_params, calendar_params, period, format=format
    )
    printer.print_events(format)


def gcal_notifier() -> NoReturn:
    """Run gcal_notifier cli.
    """

    args = cli()
    general_params, calendar_params = init_config()
    if "period" in args:
        period = define_period(args.period)
    else:
        period = define_period()

    if args.command == "get":
        run_getter(general_params, calendar_params, period)
    elif args.command == "notify":
        run_notifier(general_params, calendar_params)
    elif args.command == "print":
        run_printer(general_params, calendar_params, period, args.period)
