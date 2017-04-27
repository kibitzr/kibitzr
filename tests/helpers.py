from kibitzr.conf import ReloadableSettings


class SettingsMock(ReloadableSettings):

    def __init__(self):
        self.checks = []
        self.notifiers = {}
        self.creds = {}

    @classmethod
    def instance(cls):
        ReloadableSettings._instance = cls()
        return ReloadableSettings._instance
