import tempfile
import logging
import traceback

import sh
from ..conf import settings


logger = logging.getLogger(__name__)
PYTHON_ERROR = "script.python must set global variables ok and content"


def fetch_by_script(conf, **_kwargs):
    code = conf['script']
    try:
        python_code = code['python']
    except (KeyError, TypeError):
        # Not a python script
        pass
    else:
        return fetch_by_python(python_code, conf)
    try:
        # Explicit notation:
        bash_script = code['bash']
    except (KeyError, TypeError):
        bash_script = code
    return fetch_by_bash(bash_script)


def fetch_by_bash(code):
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


def fetch_by_python(code, conf):
    logger.info("Fetch using Python script")
    logger.debug(code)
    assert 'ok' in code, PYTHON_ERROR
    assert 'content' in code, PYTHON_ERROR
    try:
        # ok, content = False, None
        namespace = {}
        exec(code, {'conf': conf, 'creds': settings().creds}, namespace)
        return namespace['ok'], namespace['content']
    except:
        logger.exception("Python fetcher raised an Exception")
        return False, traceback.format_exc()
