import collections
import logging
import re

import six
import pytimeparse
import schedule

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)

TimelineRule = collections.namedtuple("TimelineRule", "interval unit at")


class Timeline(object):
    RE_TIME = re.compile(r'\d?\d:\d\d')

    def __init__(self, scheduler=None):
        self.scheduler = scheduler or schedule.default_scheduler

    @classmethod
    def parse_check(cls, check):
        check_schedule = []
        if "period" not in check and "schedule" not in check:
            check_schedule.append(TimelineRule(
                interval=300,
                unit='seconds',
                at=None
            ))
        elif "period" in check:
            period = check["period"]
            if isinstance(period, six.string_types):
                seconds = int(pytimeparse.parse(period))
                logger.debug('Parsed "%s" to %d seconds', period, seconds)
                period = seconds
            check_schedule.append(TimelineRule(
                interval=period,
                unit='seconds',
                at=None
            ))
        if "schedule" in check:
            schedule_value = check['schedule']
            if isinstance(schedule_value, dict):
                check_schedule.append(
                    cls._clean_single_schedule(check, schedule_value)
                )
            elif isinstance(schedule_value, list):
                check_schedule.extend([
                    cls._clean_single_schedule(check, item)
                    for item in schedule_value
                ])
            else:
                raise ConfigurationError(
                    'Check {0} has invalid schedule configuration: {1}'
                    .format(check['name'], check['schedule'])
                )
        return check_schedule

    @classmethod
    def _clean_single_schedule(cls, check, schedule_dict):
        if not isinstance(schedule_dict, dict):
            raise ConfigurationError(
                'Check {0} has invalid schedule configuration: {1}'
                .format(check['name'], schedule_dict),
            )
        try:
            every = schedule_dict['every']
        except KeyError:
            raise ConfigurationError(
                "Check {0} has invalid schedule format: {1}"
                .format(check['name'], schedule_dict)
            )
        if isinstance(every, six.string_types):
            # "every: day" shortcut
            unit, every = every, 1
        else:
            unit = schedule_dict.get('unit')
        unit = cls._clean_unit(check, unit)
        at = cls._clean_at(check, schedule_dict.get('at'))
        rule = TimelineRule(every, unit, at)
        logger.debug('Parsed schedule "%r" to %r', schedule_dict, rule)
        return rule

    @staticmethod
    def _clean_unit(check, unit):
        try:
            getattr(schedule.every(1), unit)
        except:
            raise ConfigurationError(
                "Unit {0} is not one of valid options. Referenced in check {1}"
                .format(unit, check['name'])
            )
        return unit

    @classmethod
    def _clean_at(cls, check, at):
        if at is None or cls.RE_TIME.match(at):
            return at
        raise ConfigurationError(
            'Check {0} schedule has invalid value for "at": {1}'
            .format(check['name'], at)
        )

    def schedule_checks(self, checkers):
        self.scheduler.clear()
        for checker in checkers:
            conf = checker.conf
            for s in conf['schedule']:
                job = getattr(self.scheduler.every(s.interval), s.unit)
                if s.at is not None:
                    logger.info(
                        "Scheduling checks for %r every %r %s at %r",
                        conf["name"],
                        s.interval,
                        s.unit,
                        s.at
                    )
                    job.at(s.at)
                else:
                    logger.info(
                        "Scheduling checks for %r every %r %s",
                        conf["name"],
                        s.interval,
                        s.unit,
                    )
                # Add job to scheduler
                job.do(checker.check)


# The following methods are shortcuts for not having to
# create a Timeline instance:

# default_timeline explicitly uses the default scheduler
default_timeline = Timeline()


def parse_check(check):
    return default_timeline.parse_check(check)


def run_pending():
    return default_timeline.scheduler.run_pending()


def schedule_checks(checkers):
    default_timeline.schedule_checks(checkers)
