import sh
import tempfile
import logging


logger = logging.getLogger(__name__)


class BashNotify(object):

    def __init__(self, conf, value):
        self.code = value

    def __call__(self, report):
        logger.info("Executing custom notifier")
        logger.debug(self.code)
        with tempfile.NamedTemporaryFile() as fp:
            logger.debug("Saving code to %r", fp.name)
            fp.write(self.code.encode('utf-8'))
            fp.flush()
            logger.debug("Launching script %r", fp.name)
            result = sh.bash(fp.name, _in=report)
            logger.debug("Bash exit_code: %r", result.exit_code)
            logger.debug("Bash stdout: %s", result.stdout.decode('utf-8'))
            logger.debug("Bash stderr: %s", result.stderr.decode('utf-8'))


def notify_factory(conf, value):
    return BashNotify(conf, value)
