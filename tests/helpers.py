import contextlib
import tempfile

from kibitzr.conf import ReloadableSettings
from kibitzr.stash import Stash

from .compat import mock


class SettingsMock(ReloadableSettings):

    def __init__(self):
        self.checks = []
        self.notifiers = {}
        self.creds = {'pass': 'password'}

    @classmethod
    def instance(cls):
        ReloadableSettings._instance = cls()
        return ReloadableSettings._instance

    @staticmethod
    def dispose():
        ReloadableSettings._instance = None


@contextlib.contextmanager
def stash_mock():
    with tempfile.NamedTemporaryFile() as fp:
        fp.close()
        with mock.patch.object(Stash, 'FILENAME', fp.name):
            yield Stash()
