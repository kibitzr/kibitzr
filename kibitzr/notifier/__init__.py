from .factory import CompositeNotifier


def notify_factory(conf):
    return CompositeNotifier(conf)
