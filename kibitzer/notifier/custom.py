import logging

from ..conf import settings


logger = logging.getLogger(__name__)


def post_python(conf, code, report, **kwargs):
    logger.info("Executing custom notifier")
    logger.debug(code)
    exec(code, {'text': report, 'conf': conf, 'creds': settings().creds})
