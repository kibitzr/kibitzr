import click

from webwatcher.main import main as webwatcher_main


@click.command()
def main(args=None):
    """Console script for webwatcher"""
    webwatcher_main()


if __name__ == "__main__":
    main()
