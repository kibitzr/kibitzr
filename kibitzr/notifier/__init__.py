import logging
import pkgutil
import importlib


logger = logging.getLogger(__name__)


def dummy_notify_factory(notify_func):
    def factory(conf, value):
        return notify_func
    return factory


def load_notifiers():
    path = pkgutil.extend_path(__path__, __name__)
    prefix = __name__ + '.'
    registry = {}
    for importer, modname, ispkg in pkgutil.walk_packages(path, prefix):
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


def create_notifier(name, conf, value):
    try:
        notify_factory = REGISTRY[name]
    except KeyError:
        logger.error("Unknown notifier %r", name)
        return None
    else:
        return notify_factory(conf=conf, value=value)


REGISTRY = load_notifiers()
