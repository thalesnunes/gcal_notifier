import argparse


def init_parser() -> argparse.ArgumentParser:
    """Initializes the command line parser.add()

    Returns:
        argparse.ArgumentParser: Command line parser with added arguments
    """
    main_parser = argparse.ArgumentParser(
        prog="gcal_notifier",
        description="A simple and lightweight GoogleCalendar notifier for Linux.",  # noqa
    )

    subparsers = main_parser.add_subparsers(
        help="Invoking a subcommand with --help prints subcommand usage.",
        dest="command",
    )
    subparsers.required = True

    subparsers.add_parser(
        "get",
        help="fetch events from Google Calendar and save them in cache.",
        description="Fetch events from Google Calendar and save them in cache.",  # noqa
    )

    subparsers.add_parser(
        "notify",
        help="run reminders with cached events.",
        description="Run reminders with cached events.",
    )

    parser_print = subparsers.add_parser(
        "print",
        help="print events to the console.",
        description="Print events to the console.",
    )
    parser_print.add_argument(
        "period",
        type=str,
        action="store",
        choices=["day", "week", "month", "d", "w", "m"],
        nargs="?",
        default="day",
    )

    return main_parser


def cli() -> argparse.Namespace:
    """gcal_notifier cli tool.

    Returns:
        argparse.Namespace: Namespace with parsed args from cli
    """

    parser = init_parser()
    args = parser.parse_args()

    return args
