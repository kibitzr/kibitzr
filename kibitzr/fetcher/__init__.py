from .browser import firefox_fetcher, cleanup  # noqa
from .simple import simple_fetcher, SessionFetcher  # noqa
from .shell import fetch_bash  # noqa


def cleanup_fetchers():
    cleanup()
