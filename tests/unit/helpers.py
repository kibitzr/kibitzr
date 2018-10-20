import contextlib

from kibitzr.conf import (
    ReloadableSettings,
    PlainYamlCreds,
)
from ..compat import mock


@contextlib.contextmanager
def patch_creds(data):
    with patch_source(PlainYamlCreds, 'open_creds', data) as fake_method:
        yield fake_method


@contextlib.contextmanager
def patch_conf(data):
    with patch_source(ReloadableSettings, 'open_conf', data) as fake_method:
        yield fake_method


@contextlib.contextmanager
def patch_source(klass, method, data):
    fake_file = mock.mock_open(read_data=data)
    with mock.patch.object(klass,
                           method,
                           fake_file,
                           create=True) as fake_method:
        yield fake_method
