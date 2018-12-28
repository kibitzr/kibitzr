from ..bash import execute_bash


class BashNotify(object):

    def __init__(self, value):
        self.code = value

    def __call__(self, report):
        execute_bash(self.code, report)


def register(registry):
    registry['shell'] = registry['bash'] = notify_factory


def notify_factory(conf, value):
    return BashNotify(value)
