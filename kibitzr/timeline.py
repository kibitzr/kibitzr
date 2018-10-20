import logging
import six
import collections

import pytimeparse
import schedule

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)

TimelineRule = collections.namedtuple("TimelineRule", "interval unit at")


class Timeline(object):
    def __init__(self, scheduler):
        self.scheduler = scheduler

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
                logger.debug('Parsed "%s" to %d seconds',
                             period, seconds)
                period = seconds
            check_schedule.append(TimelineRule(
                interval=period,
                unit='seconds',
                at=None
            ))
        if "schedule" in check:
            try:
                # single schedule
                conf_schedule = [
                    {'every': check['schedule']['every'],
                     'unit': check['schedule'].get('unit', None),
                     'at': check['schedule'].get('at', None)}
                ]
            except TypeError:
                # multiple schedules
                conf_schedule = check['schedule']

            for s in conf_schedule:
                if isinstance(s['every'], six.string_types):
                    unit = s['every']
                    interval = 1
                else:
                    unit = s['unit']
                    interval = s['every']
                at = s.get('at', None)

                try:
                    getattr(schedule.every(1), unit)
                except:
                    raise ConfigurationError(
                        "Unit %r not valid. Referenced in check %r"
                        % (unit, check['name'])
                    )

                check_schedule.append(TimelineRule(
                    interval=interval,
                    unit=unit,
                    at=at
                ))
                logger.debug('Parsed "%s" to %r',
                             s, check_schedule[-1])
        return check_schedule

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
default_timeline = Timeline(schedule.default_scheduler)


def parse_check(check):
    return default_timeline.parse_check(check)


def run_pending():
    return default_timeline.scheduler.run_pending()


def schedule_checks(checkers):
    default_timeline.schedule_checks(checkers)
