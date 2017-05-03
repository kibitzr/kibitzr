import pytest
from kibitzr import main
from ..compat import mock
from ..helpers import SettingsMock


@pytest.fixture(autouse=True)
def settings():
    """Override native settings singleton with empty one"""
    SettingsMock.instance()


@pytest.fixture(autouse=True)
def check_noop(mocker):
    """Cancel all side-effects from checks"""
    mocker.patch("kibitzr.main.Checker.check", spec=True)


def test_loop_aborts_without_checks():
    assert 1 == main.main()


@mock.patch.object(main, "check_forever", side_effect=main.on_interrupt)
def test_main_executes_all_checks_before_loop(the_loop):
    main.settings().checks.append({
        'name': 'A',
        'script': {'python': 'ok, content = True, "ok"'}
    })
    assert 0 == main.main()
    assert the_loop.call_count == 1
    assert the_loop.call_args[0][0][0].check.call_count == 1


def test_dummy_schedule():
    main.Checker.check.side_effect = interrupt_on_nth_call(2)
    main.settings().checks.append({
        'name': 'A',
        'script': {'python': 'ok, content = True, "ok"'},
        'period': 0,
    })
    assert 0 == main.main()
    assert main.Checker.check.call_count == 2


def interrupt_on_nth_call(n):
    def interrupter(*args, **kwargs):
        if interrupter.n > 1:
            interrupter.n -= 1
        else:
            main.on_interrupt()
        return None
    interrupter.n = n
    return interrupter


@mock.patch.object(main, "check_forever", side_effect=main.on_interrupt)
def test_main_filters_names(the_loop):
    main.settings().checks.extend([
        {'name': 'A', 'url': 'A'},
        {'name': 'B', 'url': 'B'},
    ])
    assert 0 == main.main(names=['B'])
    assert the_loop.call_count == 1
    assert the_loop.call_args[0][0][0].check.call_count == 1
