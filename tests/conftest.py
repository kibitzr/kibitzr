import pytest
from .target.server import start_server, stop_server
from kibitzr.fetcher import cleanup_fetchers
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


server_addess = None


class SettingsMock(object):
    def __init__(self):
        self.pages = []
        self.notifiers = {}
        self.creds = {}


@pytest.fixture(scope="session", autouse=True)
def target_website(request):
    global server_addess
    server_process, server_addess = start_server()
    request.addfinalizer(cleanup_fetchers)
    request.addfinalizer(lambda: stop_server(server_process))
    patch_object = patch("kibitzr.fetcher.browser.settings",
                         return_value=SettingsMock())
    patch_object.start()
    request.addfinalizer(lambda: patch_object.stop())


@pytest.fixture
def target():
    global server_addess
    return server_addess


@pytest.fixture
def json_conf(target):
    return {
        'name': 'Test page',
        'url': "http://{0}:{1}/api.json".format(*target),
        'transform': ['json'],
    }


@pytest.fixture
def html_text_conf(target):
    return {
        'name': 'Index',
        'url': "http://{0}:{1}/index.html".format(*target),
        'transform': ['text'],
    }
