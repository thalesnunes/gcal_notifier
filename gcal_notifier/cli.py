import argparse
from typing import Any, NoReturn


def init_parser() -> argparse.ArgumentParser:
    """Initializes the command line parser.add()

    Returns:
        argparse.ArgumentParser: Command line parser with added arguments
    """
    parser = argparse.ArgumentParser(
        prog="gcal_notifier",
        description="A simple and lightweight GoogleCalendar notifier for Linux",  # noqa
    )
    parser.add_argument(
        "command",
        metavar="[get|remind]",
        help='Use "get" to get events and "remind" to run reminders',
    )
    return parser


def validate_args(args: Any) -> NoReturn:
    """Validates args passed to the cli.

    Args:
        args (Any): Args passed
    """
    assert args.command in ["get", "remind", "print"], "INVALID OPTION"


def cli() -> argparse.Namespace:
    """gcal_notifier cli tool."""

    parser = init_parser()
    args = parser.parse_args()

    validate_args(args)

    return args
