from .browser import firefox_fetcher, cleanup  # noqa
from .simple import simple_fetcher, SessionFetcher  # noqa
from .script import fetch_by_script  # noqa


def cleanup_fetchers():
    cleanup()
