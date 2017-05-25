from kibitzr.stash import Stash
from kibitzr.transformer.jinja_transform import JinjaTransform


class StashNotify(Stash):

    def __init__(self, conf, value):
        super(StashNotify, self).__init__()
        self.conf = conf
        self.data = value

    def render(self, report):
        context = None
        new_values = {}
        for key, code in self.data.items():
            transform = JinjaTransform(code, self.conf)
            if context is None:
                context = transform.context(report)
            ok, value = transform.render(report, context)
            if ok:
                new_values[key] = value
            else:
                return False, {}
        return True, new_values

    def save_report(self, report):
        ok, new_values = self.render(report)
        if ok:
            self.write(new_values)
    __call__ = save_report


notify_factory = StashNotify
