from .browser import firefox_fetcher, cleanup, persistent_firefox  # noqa
from .simple import SessionFetcher  # noqa
from .script import fetch_by_script  # noqa


def cleanup_fetchers():
    cleanup()
