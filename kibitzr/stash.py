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


class LazyStash(Stash):
    def __init__(self):
        self._stash = None

    @property
    def stash(self):
        if self._stash is None:
            self._stash = self.read()
        return self._stash

    def __getitem__(self, key):
        return self.stash[key]
