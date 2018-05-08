import contextlib
import logging


logger = logging.getLogger(__name__)


class Stash(object):

    FILENAME = 'stash.db'

    @contextlib.contextmanager
    def open(self):
        import shelve
        with contextlib.closing(shelve.open(self.FILENAME)) as db:
            yield db

    def read(self):
        with self.open() as db:
            return dict(db)

    def write(self, data):
        with self.open() as db:
            for key, value in data.items():
                db[key] = value

    @classmethod
    def print_content(cls):
        for key, value in cls().read().items():
            print("{0}: {1}".format(key, value))


class LazyStash(Stash):
    def __init__(self):
        self._stashobj = None

    @property
    def _stash(self):
        if self._stashobj is None:
            self._stashobj = self.read()
        return self._stashobj

    def __getitem__(self, key):
        return self._stash[key]

    def get(self, key, default=None):
        try:
            return self._stash[key]
        except KeyError:
            return default
