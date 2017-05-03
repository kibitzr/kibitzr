from .factory import fetcher_factory  # noqa
from .browser import (  # noqa
    cleanup,
    persistent_firefox,
)


def cleanup_fetchers():
    cleanup()
