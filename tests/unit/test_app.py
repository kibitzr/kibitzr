from ..compat import mock


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


def test_main_filters_names(app, settings):
    with mock.patch.object(app, "check_forever", side_effect=app.on_interrupt) as the_loop:
        settings.checks.extend([
            {'name': 'A', 'url': 'A'},
            {'name': 'B', 'url': 'B'},
        ])
        assert app.run(names=['B']) == 1
    assert the_loop.call_count == 1
    assert the_loop.call_args[0][0][0].check.call_count == 1
