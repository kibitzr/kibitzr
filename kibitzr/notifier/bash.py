from ..bash import execute_bash


class BashNotify(object):

    def __init__(self, value):
        self.code = value

    def __call__(self, report):
        execute_bash(self.code, report)


def notify_factory(conf, value):
    return BashNotify(value)
