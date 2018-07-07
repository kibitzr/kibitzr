import pytest
from kibitzr.app import Application
from ..compat import mock
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


def test_loop_aborts_without_checks(app, settings):
    assert app.run() == 1


def test_main_executes_all_checks_before_loop(app, settings):
    with mock.patch.object(app, "check_forever", side_effect=app.on_interrupt) as the_loop:
        settings.checks.append({
            'name': 'A',
            'script': {'python': 'ok, content = True, "ok"'}
        })
        assert app.run() == 1
    assert the_loop.call_count == 1
    assert the_loop.call_args[0][0][0].check.call_count == 1


def test_dummy_schedule(app, settings, check_noop):
    check_noop.side_effect = interrupt_on_nth_call(app, 2)
    settings.checks.append({
        'name': 'A',
        'script': {'python': 'ok, content = True, "ok"'},
        'period': 0,
    })
    assert 1 == app.run()
    assert check_noop.call_count == 2


def interrupt_on_nth_call(app, n):
    def interrupter(*args, **kwargs):
        if interrupter.n > 1:
            interrupter.n -= 1
        else:
            app.on_interrupt()
        return None
    interrupter.n = n
    return interrupter


def test_main_filters_names(app, settings):
    with mock.patch.object(app, "check_forever", side_effect=app.on_interrupt) as the_loop:
        settings.checks.extend([
            {'name': 'A', 'url': 'A'},
            {'name': 'B', 'url': 'B'},
        ])
        assert app.run(names=['B']) == 1
    assert the_loop.call_count == 1
    assert the_loop.call_args[0][0][0].check.call_count == 1
