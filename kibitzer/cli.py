import logging

import click

from kibitzer.main import main as kibitzer_main


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
def main(once, log_level):
    log_level_code = LOG_LEVEL_CODES[log_level]
    kibitzer_main(once=once, log_level=log_level_code)


if __name__ == "__main__":
    main()
