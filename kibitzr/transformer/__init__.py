"""
Built-in transforms
"""
import logging
import functools
import traceback
import tempfile

import six
import sh

from ..storage import PageHistory
from ..conf import settings
from .html import HTML_REGISTRY
from .json_transforms import JSON_REGISTRY


PYTHON_ERROR = "transform.python must set global variables ok and content"
logger = logging.getLogger(__name__)


def load_transforms():
    registry = {}
    registry.update(HTML_REGISTRY)
    registry.update(JSON_REGISTRY)
    registry.update({
        'changes': changes_transform_factory,
        'python': python_transform_factory,
        'bash': bash_transform_factory,
    })
    return registry


def changes_transform_factory(value, conf):
    if value and value.lower() == 'verbose':
        return functools.partial(PageHistory(conf).report_changes,
                                 verbose=True)
    else:
        return PageHistory(conf).report_changes


def pipeline_factory(conf):
    rules = conf.get('transform', [])
    if isinstance(rules, six.string_types):
        rules = [rules]
    return functools.partial(
        pipeline,
        transformers=[
            transformer_factory(conf, rule)
            for rule in rules
        ]
    )


def pipeline(ok, content, transformers):
    for transformer in transformers:
        if ok:
            ok, content = transformer(content)
        else:
            break
    return ok, content


def transformer_factory(conf, rule):
    try:
        name, value = next(iter(rule.items()))
    except AttributeError:
        name, value = rule, None
    if name == 'sort':
        return sort_lines
    elif name == 'cut':
        return functools.partial(cut_lines, value)
    else:
        try:
            return REGISTRY[name](value, conf=conf)
        except KeyError:
            raise RuntimeError(
                "Unknown transformer: %r" % (name,)
            )


def sort_lines(text):
    return True, u''.join([
        line + u'\n'
        for line in sorted(text.splitlines())
        if line
    ])


def cut_lines(last_line, text):
    return True, u''.join([
        line + u'\n'
        for line in text.splitlines()[:last_line]
    ])


def python_transform_factory(value, conf):
    return functools.partial(
        python_transform,
        code=value,
        conf=conf,
    )


def bash_transform_factory(value, conf):
    return functools.partial(
        bash_transform,
        code=value,
    )


def python_transform(content, code, conf):
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


def bash_transform(content, code):
    logger.info("Bash transform")
    logger.debug(code)
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


REGISTRY = load_transforms()
