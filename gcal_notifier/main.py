#!/usr/bin/env python
from datetime import datetime
from typing import Any, Dict, Tuple

from gcal_notifier.cli import cli
from gcal_notifier.config_reader import init_config
from gcal_notifier.event_getter import SimpleGCalendarGetter
from gcal_notifier.event_loader import load_saved_events
from gcal_notifier.event_printer import SimpleGCalendarPrinter
from gcal_notifier.event_reminder import SimpleGCalendarNotifier
from gcal_notifier.event_saver import save_events
from gcal_notifier.globals import CACHE
from gcal_notifier.utils import define_period


def run_getter(
    general_params: Dict[str, Any],
    calendar_params: Dict[str, Any],
) -> None:
    """Run SimpleGCalendarGetter with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
    """
    getter = SimpleGCalendarGetter(general_params, calendar_params)

    getter.load_calendars(define_period("day"))
    getter.load_events()
    save_events(getter.events, file_path=CACHE / "events_notify.json")

    getter.load_calendars(define_period("month"))
    getter.load_events()
    save_events(getter.events, file_path=CACHE / "events_print.json")


def run_notifier(
    general_params: Dict[str, Any], calendar_params: Dict[str, Any]
) -> None:
    """Run SimpleGCalendarNotifier with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
    """
    saved_events = load_saved_events(CACHE / "events_notify.json")
    notifier = SimpleGCalendarNotifier(
        saved_events, general_params, calendar_params
    )
    notifier.search_reminders()


def run_printer(
    general_params: Dict[str, Any],
    calendar_params: Dict[str, Any],
    period: Tuple[datetime, datetime],
    format: str = "day",
) -> None:
    """Run SimpleGCalendarPrinter with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
        format (str): Format to use when printing events
    """
    saved_events = load_saved_events(CACHE / "events_print.json")
    printer = SimpleGCalendarPrinter(
        saved_events, general_params, calendar_params, period, format=format
    )
    printer.print_events(format)


def gcal_notifier() -> None:
    """Run gcal_notifier cli."""

    args = cli()
    general_params, calendar_params = init_config()

    if args.command == "get":
        run_getter(general_params, calendar_params)
    elif args.command == "notify":
        run_notifier(general_params, calendar_params)
    elif args.command == "print":
        period = define_period(args.period)
        run_printer(general_params, calendar_params, period, args.period)
