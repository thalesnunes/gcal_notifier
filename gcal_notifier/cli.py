import argparse
from typing import Any


def init_parser() -> argparse.ArgumentParser:
    """Initializes the command line parser.add()

    Returns:
        argparse.ArgumentParser: Command line parser with added arguments
    """
    parser = argparse.ArgumentParser(
        prog="gcal_notifier",
        description="A simple and lightweight GoogleCalendar notifier for Linux"
    )
    parser.add_argument(
        "command",
        metavar="[get|remind]",
        help='Use "get" to get events and "remind" to run reminders',
    )
    return parser


def validate_args(args: Any):
    assert args.command in ["get", "remind"], "INVALID OPTION"


def cli():

    parser = init_parser()
    args = parser.parse_args()

    validate_args(args)

    return args
