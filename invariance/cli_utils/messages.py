from __future__ import annotations

import typer
from rich import print


def info(msg: str) -> None:
    print(f"[bold green]✔[/bold green] {msg}")


def warn(msg: str) -> None:
    print(f"[bold yellow]⚠[/bold yellow] {msg}")


def error(msg: str, err: bool = True) -> None:
    from rich.console import Console
    console = Console(stderr=err)
    console.print(f"[bold red]✖[/bold red] {msg}")