import logging
import tempfile

import sh


logger = logging.getLogger(__name__)


def execute_bash(code, stdin=None):
    logger.info("Executing bash script")
    logger.debug(code)
    if stdin is not None:
        if not stdin.strip():
            logger.info("Skipping execution with empty content")
            return True, stdin
        stdin = stdin.encode("utf-8")
    with tempfile.NamedTemporaryFile() as fp:
        logger.debug("Saving code to %r", fp.name)
        fp.write(code.encode('utf-8'))
        fp.flush()
        logger.debug("Launching script %r", fp.name)
        try:
            result = sh.bash(fp.name, _in=stdin)
            ok = True
        except sh.ErrorReturnCode as exc:
            result = exc
            ok = False
    stdout = result.stdout.decode('utf-8')
    stderr = result.stderr.decode('utf-8')
    if ok:
        log = logger.debug
        report = stdout
    else:
        log = logger.error
        report = stderr
    log("Bash exit_code: %r", result.exit_code)
    log("Bash stdout: %s", stdout)
    log("Bash stderr: %s", stderr)
    return ok, report
