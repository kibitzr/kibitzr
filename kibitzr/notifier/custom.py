import logging

from ..conf import settings


logger = logging.getLogger(__name__)


def post_python(conf, code, report, **_kwargs):
    logger.info("Executing custom notifier")
    logger.debug(code)
    exec(
        code,
        {
            'text': report,  # legacy
            'content': report,
            'conf': conf,
            'creds': settings().creds,
        },
    )
