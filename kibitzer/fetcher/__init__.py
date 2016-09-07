import logging
import traceback

from .browser import firefox_fetcher, cleanup
from .simple import simple_fetcher


logger = logging.getLogger(__name__)


FETCHERS = {
    'asis': simple_fetcher,
    'json': simple_fetcher,
    'text': firefox_fetcher,
    'html': firefox_fetcher,
}


def fetch(conf):
    try:
        return FETCHERS[conf.get('format', 'asis')](conf)
    except Exception:
        logger.exception(
            "Exception occured while fetching page"
        )
        return False, traceback.format_exc()


def cleanup_fetchers():
    cleanup()
