import pytest
from freezegun import freeze_time

from kibitzr.timeline import Timeline, TimelineRule
from kibitzr.exceptions import ConfigurationError


def test_dummy_schedule(app, settings, check_noop):
    check_noop.side_effect = interrupt_on_nth_call(app, 2)
    settings.checks.append({
        'name': 'A',
        'script': {'python': 'ok, content = True, "ok"'},
        'schedule': [TimelineRule(interval=0, unit='seconds', at=None)],
    })
    assert app.run() == 1
    assert check_noop.call_count == 2


def interrupt_on_nth_call(app, n):
    def interrupter():
        if interrupter.n > 1:
            interrupter.n -= 1
        else:
            app.on_interrupt()
        return None
    interrupter.n = n
    return interrupter


def test_period_parse():
    rule = Timeline.parse_check({'period': '1 hour'})
    assert rule == [TimelineRule(interval=3600, unit='seconds', at=None)]


def test_empty_period():
    rule = Timeline.parse_check({'name': 'x'})
    assert rule == [TimelineRule(interval=300, unit='seconds', at=None)]


def test_sample_schedule():
    rule = Timeline.parse_check({
        'schedule': {
            'every': 1,
            'unit': 'week',
            'at': '07:40',
        }
    })
    assert rule == [TimelineRule(interval=1, unit='week', at='07:40')]


def test_invalid_schedule():
    with pytest.raises(ConfigurationError):
        Timeline.parse_check({
            'name': 'x',
            'schedule': 'daily',
        })


def test_invalid_unit():
    with pytest.raises(ConfigurationError):
        Timeline.parse_check({
            'name': 'x',
            'schedule': {
                'every': 2,
                'unit': 'olympics'
            },
        })


def test_invalid_every():
    with pytest.raises(ConfigurationError):
        print(Timeline.parse_check({
            'name': 'x',
            'schedule': {
                'every': 'single',  # every must be integer
                'unit': 'minute',
            },
        }))


def test_invalid_time():
    with pytest.raises(ConfigurationError):
        print(Timeline.parse_check({
            'name': 'x',
            'schedule': {
                'every': 'day',
                'at': 'noon',
            },
        }))


def test_schedule_daily_with_time():
    timeline = Timeline()
    timeline.schedule_checks([DummyCheck([
        TimelineRule(1, 'day', '12:34')
    ])])
    next_run = timeline.scheduler.jobs[0].next_run
    assert next_run.hour == 12
    assert next_run.minute == 34


@freeze_time("1945-05-09 12:34:56")
def test_schedule_daily_uses_current_time_by_default():
    timeline = Timeline()
    timeline.schedule_checks([DummyCheck([
        TimelineRule(1, 'day', None)
    ])])
    next_run = timeline.scheduler.jobs[0].next_run
    assert next_run.hour == 12
    assert next_run.minute == 34


class DummyCheck(object):
    def __init__(self, rules):
        self.conf = {
            'name': 'dummy',
            'schedule': rules,
        }

    def check(self):
        pass
