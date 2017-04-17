import sys
import logging

import click

from kibitzr import __version__ as kibitzr_version
from kibitzr.main import main, run_firefox


LOG_LEVEL_CODES = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


@click.command()
@click.option("--once", is_flag=True,
              help="Run checks once and exit")
@click.option("-l", "--log-level", default="info",
              type=click.Choice(LOG_LEVEL_CODES.keys()),
              help="Logging level")
@click.option("-v", "--version", is_flag=True,
              help="Print version and exit")
@click.option("--firefox", is_flag=True,
              help="Launch Firefox with persistent profile and exit")
@click.argument('name', nargs=-1)
def entry(once, log_level, version, firefox, name):
    """Run kibitzr in the foreground mode"""
    if version:
        print(kibitzr_version)
    elif firefox:
        run_firefox()
    else:
        log_level_code = LOG_LEVEL_CODES[log_level]
        sys.exit(main(once=once, log_level=log_level_code, names=name))


if __name__ == "__main__":
    entry()
