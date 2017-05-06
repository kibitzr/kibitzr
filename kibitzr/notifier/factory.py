import os
import logging
import pkgutil
import importlib


logger = logging.getLogger(__name__)


def dummy_notify_factory(notify_func):
    def factory(conf, value):
        return notify_func
    return factory


def load_notifiers():
    path = os.path.dirname(os.path.abspath(__file__))
    before, sep, _ = __name__.rpartition('.')
    prefix = before + sep
    registry = {}
    for _, modname, _ in pkgutil.walk_packages([path], prefix):
        submodule = importlib.import_module(modname, __name__)
        if hasattr(submodule, 'register'):
            submodule.register(registry)
        else:
            key = getattr(submodule, 'NAME', modname.split('.')[-1])
            if hasattr(submodule, 'notify_factory'):
                registry[key] = submodule.notify_factory
            elif hasattr(submodule, 'notify'):
                registry[key] = dummy_notify_factory(submodule.notify)
    return registry


class CompositeNotifier(object):

    REGISTRY = load_notifiers()

    def __init__(self, conf):
        self.conf = conf
        notifiers_conf = conf.get('notify', [])
        if not notifiers_conf:
            logger.warning(
                "No notifications configured for %r",
                conf['name'],
            )
        self.notifiers = []
        for notifier_conf in notifiers_conf:
            self.add_notifier(notifier_conf)

    def add_notifier(self, notifier_conf):
        try:
            name, value = next(iter(notifier_conf.items()))
        except AttributeError:
            name, value = notifier_conf, None
        try:
            notify_factory = self.REGISTRY[name]
        except KeyError:
            logger.error("Unknown notifier %r", name)
        else:
            self.notifiers.append(
                notify_factory(conf=self.conf, value=value)
            )

    def notify(self, report):
        if report:
            logger.debug('Sending report: %r', report)
            for notifier in self.notifiers:
                try:
                    notifier(report=report)
                except:
                    logger.exception(
                        "Exception occurred during sending notification"
                    )
        else:
            logger.debug('Report is empty, skipping notification')
    __call__ = notify
