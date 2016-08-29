import logging
import traceback

from .browser import browser
from .simple import simple


logger = logging.getLogger(__name__)


FETCHERS = {
    'asis': simple,
    'json': simple,
    'text': browser,
    'html': browser,
}


def fetch(conf):
    try:
        return FETCHERS[conf.get('format', 'asis')](conf)
    except Exception:
        logger.exception(
            "Exception occured during sending notification"
        )
        return traceback.format_exc()
