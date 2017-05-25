import logging
import traceback

import six

from kibitzr.stash import LazyStash
from kibitzr.conf import settings
from kibitzr.storage import PageHistory
from kibitzr.bash import execute_bash
from .utils import bake_parametrized


PYTHON_ERROR = "transform.python must set global variables ok and content"
logger = logging.getLogger(__name__)


def changes_transform_factory(value, conf):
    style = value.lower() if value else None
    return PageHistory(conf, style=style).report_changes


def python_transform(code, content, conf):
    logger.info("Python transform")
    logger.debug(code)
    assert 'content' in code, PYTHON_ERROR
    try:
        namespace = {'ok': True, 'content': content}
        context = {
            'conf': conf,
            'stash': LazyStash(),
            'creds': settings().creds,
        }
        exec(code, context, namespace)
        return namespace['ok'], six.text_type(namespace['content'])
    except:
        logger.exception("Python transform raised an Exception")
        return False, traceback.format_exc()


def bash_transform(code, content):
    return execute_bash(code, content)


def register():
    return {
        'changes': changes_transform_factory,
        'python': bake_parametrized(python_transform, pass_conf=True),
        'bash': bake_parametrized(bash_transform),
    }
