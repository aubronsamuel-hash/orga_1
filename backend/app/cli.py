import json
import platform
import socket
import time
from typing import Any

import typer

from . import __version__
from .config import get_settings

app = typer.Typer(add_completion=False, help="CCW CLI (Windows-first)")


@app.callback()
def _cb() -> None:
    return


@app.command()
def version() -> None:
    typer.echo(f"cc {__version__}")


@app.command()
def env() -> None:
    s = get_settings()
    typer.echo(f"env={s.app_env} log={s.log_level} tz={s.tz} req_id_header={s.request_id_header}")


@app.command()
def ping() -> None:
    typer.echo("pong")


@app.command()
def check(json_out: bool = typer.Option(False, "--json", help="Sortie JSON compacte")) -> None:
    ok = True
    details: dict[str, Any] = {
        "python": platform.python_version(),
        "host": socket.gethostname(),
        "time": int(time.time()),
    }
    if json_out:
        typer.echo(json.dumps({"ok": ok, "details": details}, separators=(",", ":")))
    else:
        typer.echo("OK" if ok else "KO")

