"""
Built-in transforms
"""
import logging

import six

from .html import HTML_REGISTRY
from .json_transforms import JSON_REGISTRY
from .plain_text import PLAIN_TEXT_REGISTRY
from .jinja_transform import JINJA_REGISTRY


logger = logging.getLogger(__name__)


def transform_factory(conf):
    return TransformPipeline(conf)


def load_transforms():
    registry = {}
    registry.update(HTML_REGISTRY)
    registry.update(JSON_REGISTRY)
    registry.update(PLAIN_TEXT_REGISTRY)
    registry.update(JINJA_REGISTRY)
    return registry


class TransformPipeline(object):

    REGISTRY = load_transforms()

    def __init__(self, conf):
        self.conf = conf
        rules = self.conf.get('transform', [])
        if isinstance(rules, six.string_types):
            rules = [rules]
        self.transforms = [
            self.create_transform(rule)
            for rule in rules
        ]

    def run_pipeline(self, ok, content):
        for transform in self.transforms:
            if ok:
                ok, content = transform(content)
            else:
                content = self.on_error(content)
        if content:
            content = content.strip()
        return ok, content
    __call__ = run_pipeline

    def create_transform(self, rule):
        try:
            name, value = next(iter(rule.items()))
        except AttributeError:
            name, value = rule, None
        try:
            return self.REGISTRY[name](value, conf=self.conf)
        except KeyError:
            raise RuntimeError(
                "Unknown transform: %r" % (name,)
            )

    def on_error(self, content):
        error_policy = self.conf.get('error', 'notify')
        if error_policy == 'ignore':
            if content:
                logger.error("Ignoring error in %s",
                             repr(content)[:60])
            return None
        elif error_policy == 'notify':
            logger.debug("Notifying on error")
            return content
        else:
            logger.warning("Unknown error policy: %r", error_policy)
            logger.info("Defaulting to 'notify'")
            return content
