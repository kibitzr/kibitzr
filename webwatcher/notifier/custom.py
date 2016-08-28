import logging

from ..settings import NOTIFIERS


logger = logging.getLogger(__name__)


def post_python(code, report):
    if code in NOTIFIERS:
        code = NOTIFIERS[code]
    logger.info("Executing custom notifier")
    logger.debug(code)
    exec(code, {'text': report})
