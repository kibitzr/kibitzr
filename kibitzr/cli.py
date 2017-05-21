import sys
import logging

import click


LOG_LEVEL_CODES = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


@click.group()
@click.option("-l", "--log-level", default="info",
              type=click.Choice(LOG_LEVEL_CODES.keys()),
              help="Logging level")
@click.pass_context
def cli(ctx, log_level):
    """Run kibitzr COMMAND --help for detailed descriptions"""
    ctx.obj = {'log_level': LOG_LEVEL_CODES[log_level.lower()]}


@cli.command()
def version():
    """Print version"""
    from kibitzr import __version__ as kibitzr_version
    print(kibitzr_version)


@cli.command()
def firefox():
    """Launch Firefox with persistent profile"""
    from kibitzr.main import run_firefox
    run_firefox()


@cli.command()
@click.argument('name', nargs=-1)
@click.pass_context
def once(ctx, name):
    """Run kibitzr checks once and exit"""
    from kibitzr.main import main
    sys.exit(main(once=True, log_level=ctx.obj['log_level'], names=name))


@cli.command()
@click.argument('name', nargs=-1)
@click.pass_context
def run(ctx, name):
    """Run kibitzr in the foreground mode"""
    from kibitzr.main import main
    sys.exit(main(once=False, log_level=ctx.obj['log_level'], names=name))


@cli.command()
def init():
    """Create boilerplate configuration files"""
    from kibitzr.main import bootstrap
    bootstrap()


@cli.command()
def telegram_chat():
    """Return chat id for the last message sent to Telegram Bot"""
    from kibitzr.main import telegram_chat
    telegram_chat()


if __name__ == "__main__":
    cli()
