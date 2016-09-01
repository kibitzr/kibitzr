import sh
import tempfile
import logging


logger = logging.getLogger(__name__)


def post_bash(code, report):
    logger.info("Executing custom notifier")
    logger.debug(code)
    with tempfile.NamedTemporaryFile() as fp:
        logger.debug("Saving code to %r", fp.name)
        fp.write(code.encode('utf-8'))
        fp.flush()
        logger.debug("Launching script %r", fp.name)
        logger.info(sh.bash(fp.name, _in=report))
