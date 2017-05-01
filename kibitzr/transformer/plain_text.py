import logging
import traceback
import tempfile

import six
import sh

from ..conf import settings
from ..storage import PageHistory
from .utils import bake_parametrized


PYTHON_ERROR = "transform.python must set global variables ok and content"
logger = logging.getLogger(__name__)


def changes_transform_factory(value, conf):
    style = value.lower() if value else None
    return PageHistory(conf, style=style).report_changes


def python_transform(code, content, conf):
    logger.info("Python transform")
    logger.debug(code)
    assert 'ok' in code, PYTHON_ERROR
    assert 'content' in code, PYTHON_ERROR
    try:
        namespace = {'content': content}
        exec(code, {'creds': settings().creds, 'conf': conf}, namespace)
        return namespace['ok'], six.text_type(namespace['content'])
    except:
        logger.exception("Python transform raised an Exception")
        return False, traceback.format_exc()


def bash_transform(code, content):
    logger.info("Bash transform")
    logger.debug(code)
    if not content.strip():
        logger.info("Skipping transform for empty content")
        return True, content
    with tempfile.NamedTemporaryFile() as fp:
        logger.debug("Saving code to %r", fp.name)
        fp.write(code.encode('utf-8'))
        fp.flush()
        logger.debug("Launching script %r", fp.name)
        result = sh.bash(fp.name, _in=content.encode('utf-8'))
        logger.debug("Bash exit_code: %r", result.exit_code)
        logger.debug("Bash stdout: %s", result.stdout.decode('utf-8'))
        logger.debug("Bash stderr: %s", result.stderr.decode('utf-8'))
    return True, result.stdout.decode('utf-8')


PLAIN_TEXT_REGISTRY = {
    'changes': changes_transform_factory,
    'python': bake_parametrized(python_transform, pass_conf=True),
    'bash': bake_parametrized(bash_transform),
}
