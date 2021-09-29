from typing import Any, Dict

from rich.console import Console
from rich.table import Table


def create_columns(table: Table, **columns: Dict[str, Any]):
    for name, attrs in columns.items():
        table.add_column(name, **attrs)


def add_rows(table: Table, **rows: Dict[str, Any]):
    for name, attrs in rows.items():
        table.add_row(name, **attrs)


def print_cal():

    console = Console()

    table = Table(show_header=True, header_style="bold")
    table.add_row(
        "Dev 20, 2019",
        "Star Wars: The Rise of Skywalker",
        "$275,000,0000",
        "$375,126,118"
    )
    table.add_row(
        "May 25, 2018",
        "[red]Solo[/red]: A Star Wars Story",
        "$275,000,0000",
        "$393,151,347",
    )
    table.add_row(
        "Dec 15, 2017",
        "Star Wars Ep. VIII: The Last Jedi",
        "$262,000,000",
        "[bold]$1,332,539,889[/bold]",
    )

    console.print(table)
