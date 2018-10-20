import pytest
from kibitzr.app import Application
from ..helpers import SettingsMock


@pytest.fixture(scope="function")
def settings(request):
    """Override native settings singleton with empty one"""
    instance = SettingsMock.instance()
    request.addfinalizer(SettingsMock.dispose)
    return instance


@pytest.fixture(autouse=True)
def check_noop(mocker):
    """Cancel all side-effects from checks"""
    return mocker.patch("kibitzr.app.Checker.check", spec=True)


@pytest.fixture
def app():
    return Application()
