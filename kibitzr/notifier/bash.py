import sh
import tempfile
import logging


logger = logging.getLogger(__name__)


def post_bash(code, report, **kwargs):
    logger.info("Executing custom notifier")
    logger.debug(code)
    with tempfile.NamedTemporaryFile() as fp:
        logger.debug("Saving code to %r", fp.name)
        fp.write(code.encode('utf-8'))
        fp.flush()
        logger.debug("Launching script %r", fp.name)
        result = sh.bash(fp.name, _in=report)
        logger.debug("Bash exit_code: %r", result.exit_code)
        logger.debug("Bash stdout: %s", result.stdout.decode('utf-8'))
        logger.debug("Bash stderr: %s", result.stderr.decode('utf-8'))
