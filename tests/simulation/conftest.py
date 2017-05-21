import pytest
from .target.server import start_server, stop_server
from kibitzr.fetcher import cleanup_fetchers
from ..compat import mock
from ..helpers import SettingsMock


server_address = None


@pytest.fixture(scope="session", autouse=True)
def target_website(request):
    global server_address
    server_process, server_address = start_server()
    request.addfinalizer(cleanup_fetchers)
    request.addfinalizer(lambda: stop_server(server_process))
    for module in ("browser.fetcher", "script"):
        patch_object = mock.patch(
            "kibitzr.fetcher.%s.settings" % module,
            return_value=SettingsMock()
        )
        patch_object.start()
        request.addfinalizer(patch_object.stop)


@pytest.fixture
def target():
    global server_address
    return server_address


@pytest.fixture
def not_found_conf(target):
    return {
        'name': '404',
        'url': "http://{0}:{1}/page-not-found".format(*target),
    }


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


@pytest.fixture()
def python_script_conf():
    return {
        'name': 'Echo',
        'script': {'python': 'ok, content = True, "python"'},
    }
