import pytest
from target.server import start_server
from webwatcher.fetcher import cleanup_fetchers


server_addess = None


@pytest.fixture(scope="session", autouse=True)
def target_website(request):
    global server_addess
    server_addess = start_server()
    request.addfinalizer(cleanup_fetchers)


@pytest.fixture
def target():
    global server_addess
    return server_addess


@pytest.fixture
def json_conf(target):
    return {
        'name': 'Test page',
        'url': "http://{0}:{1}/api.json".format(*target),
        'format': 'json',
    }


@pytest.fixture
def html_text_conf(target):
    return {
        'name': 'Index',
        'url': "http://{0}:{1}/index.html".format(*target),
        'format': 'text',
    }
