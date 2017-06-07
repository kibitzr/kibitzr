import logging
import traceback

from ..conf import settings
from ..bash import execute_bash
from ..stash import LazyStash


logger = logging.getLogger(__name__)
PYTHON_ERROR = "script.python must set global variables ok and content"


def fetch_by_script(conf):
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
    # Pass something to stdin to disable sanity check:
    return execute_bash(
        bash_script,
        conf.get('name', 'dummy'),
    )


def fetch_by_python(code, conf):
    logger.info("Fetch using Python script")
    logger.debug(code)
    assert 'content' in code, PYTHON_ERROR
    try:
        # ok, content = False, None
        namespace = {'ok': True}
        context = {
            'conf': conf,
            'stash': LazyStash(),
            'creds': settings().creds,
        }
        exec(code, context, namespace)
        return namespace['ok'], namespace['content']
    except:
        logger.exception("Python fetcher raised an Exception")
        return False, traceback.format_exc()
