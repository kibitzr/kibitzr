"""
Built-in transforms
"""
import os
import pkgutil
import importlib
import logging

import six


logger = logging.getLogger(__name__)


def transform_factory(conf):
    return TransformPipeline(conf)


def load_transforms():
    path = os.path.dirname(os.path.abspath(__file__))
    before, sep, _ = __name__.rpartition('.')
    prefix = before + sep
    registry = {}
    for _, modname, _ in pkgutil.walk_packages([path], prefix):
        submodule = importlib.import_module(modname, __name__)
        if hasattr(submodule, 'register'):
            registry.update(submodule.register())
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
                break
        if not ok:
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
