import logging


logger = logging.getLogger(__name__)


def post_python(code, report):
    logger.info("Executing custom notifier")
    logger.debug(code)
    exec(code, {'text': report})
