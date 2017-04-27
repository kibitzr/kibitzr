from .simple import SessionFetcher  # noqa
from .script import fetch_by_script  # noqa
from .browser import (  # noqa
    firefox_fetcher,
    cleanup,
    persistent_firefox,
    needs_firefox,
)


def cleanup_fetchers():
    cleanup()
