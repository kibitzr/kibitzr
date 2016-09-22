import sh
import tempfile
import logging


logger = logging.getLogger(__name__)


def fetch_bash(conf, **kwargs):
    code = conf['script']
    logger.info("Executing bash fetcher")
    logger.debug(code)
    with tempfile.NamedTemporaryFile() as fp:
        logger.debug("Saving code to %r", fp.name)
        fp.write(code.encode('utf-8'))
        fp.flush()
        logger.debug("Launching script %r", fp.name)
        result = sh.bash(fp.name)
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        logger.debug("Bash exit_code: %r", result.exit_code)
        logger.debug("Bash stdout: %s", stdout)
        logger.debug("Bash stderr: %s", stderr)
        ok = (result.exit_code == 0)
        if ok:
            report = stdout
        else:
            report = u'\n'.join([stdout, stderr])
        return ok, report
