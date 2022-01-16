#!/usr/bin/env python
from typing import Any, Dict, NoReturn

from gcal_notifier.cli import cli
from gcal_notifier.config_reader import init_config
from gcal_notifier.event_getter import SimpleGCalendarGetter
from gcal_notifier.event_loader import load_saved_events
from gcal_notifier.event_printer import SimpleGCalendarPrinter
from gcal_notifier.event_reminder import SimpleGCalendarNotifier
from gcal_notifier.event_saver import save_events


def run_getter(
    general_params: Dict[str, Any], calendar_params: Dict[str, Any]
) -> NoReturn:
    """Run SimpleGCalendarGetter with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
    """
    getter = SimpleGCalendarGetter(general_params, calendar_params)
    getter.load_calendars()
    getter.load_events()
    save_events(getter.events)


def run_notifier(
    general_params: Dict[str, Any], calendar_params: Dict[str, Any]
) -> NoReturn:
    """Run SimpleGCalendarNotifier with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
    """
    saved_events = load_saved_events()
    SimpleGCalendarNotifier(saved_events, general_params, calendar_params)


def run_printer(
    general_params: Dict[str, Any], calendar_params: Dict[str, Any]
) -> NoReturn:
    """Run SimpleGCalendarNotifier with user configs.

    Args:
        general_params (Dict[str, Any]): General params
        calendar_params (Dict[str, Any]): Calendar params
    """
    saved_events = load_saved_events()
    printer = SimpleGCalendarPrinter(
        saved_events, general_params, calendar_params
    )
    printer.tabulate_events()


def gcal_notifier() -> NoReturn:
    """Run gcal_notifier cli."""

    args = cli()
    general_params, calendar_params = init_config()

    if args.command == "get":
        run_getter(general_params, calendar_params)
    elif args.command == "remind":
        run_notifier(general_params, calendar_params)
    elif args.command == "print":
        run_printer(general_params, calendar_params)
