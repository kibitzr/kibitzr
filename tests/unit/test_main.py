import pytest
from kibitzr import main
from ..compat import mock
from ..helpers import SettingsMock


def test_main_executes_all_checks_before_loop():
    settings = SettingsMock()
    with mock.patch.object(main, "settings") as fake_settings:
        fake_settings.return_value = settings
        with mock.patch.object(main, "Checker") as checker:
            main.main(once=True)
    assert checker.call_count == 0  # hahaha


def test_loop_aborts_without_checks():
    settings = SettingsMock()
    with mock.patch.object(main, "settings") as fake_settings:
        fake_settings.return_value = settings
        with pytest.raises(SystemExit):
            main.main()
