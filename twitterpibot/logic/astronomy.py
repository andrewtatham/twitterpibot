import astral
import datetime
import logging

import pytz

logger = logging.getLogger(__name__)


def get_times(day):
    a = astral.Astral()
    city = a['Leeds']
    sun = city.sun(date=day, local=False)

    logger.debug("dawn: " + str(sun['dawn']))
    logger.debug("sunrise: " + str(sun['sunrise']))
    logger.debug("noon: " + str(sun['noon']))
    logger.debug("sunset: " + str(sun['sunset']))
    logger.debug("dusk: " + str(sun['dusk']))
    return sun


def get_today_times(today=None):
    if not today:
        today = datetime.date.today(pytz.UTC)
    return get_times(today)


def get_tomorrow_times(today=None):
    if not today:
        today = datetime.date.today(pytz.UTC)
    return get_times(today + datetime.timedelta(days=1))


def _interpolate(start_date, now, end_date):
    return (end_date - now) / (end_date - start_date)


def get_daytimeness_factor(now=None):
    if not now:
        now = datetime.datetime.now(pytz.UTC)
    today = now.today()

    today_times = get_today_times(today)
    tomorrow_times = get_tomorrow_times(today)

    if now <= today_times["dawn"]:
        return 0
    elif today_times["dawn"] <= now < today_times["sunrise"]:
        return 1 - _interpolate(today_times["dawn"], now, today_times["sunrise"])
    elif today_times["sunrise"] <= now < today_times["sunset"]:
        return 1
    elif today_times["sunset"] <= now < today_times["dusk"]:
        return _interpolate(today_times["sunset"], now, today_times["dusk"])
    elif today_times["dusk"] <= now < tomorrow_times["dawn"]:
        return 0
    elif tomorrow_times["dawn"] <= now < tomorrow_times["sunrise"]:
        return 1 - _interpolate(tomorrow_times["dawn"], now, tomorrow_times["sunrise"])
    elif tomorrow_times["sunrise"] <= now < tomorrow_times["sunset"]:
        return 1
    elif tomorrow_times["sunset"] <= now < tomorrow_times["dusk"]:
        return _interpolate(tomorrow_times["sunset"], now, tomorrow_times["dusk"])
    else:
        return 0


if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    now = datetime.datetime.now(pytz.UTC)

    for hour in range(24):
        for min in range(0, 59, 5):
            time = now + datetime.timedelta(hours=hour, minutes=min)

            print("{} {} {}".format(hour, time, get_daytimeness_factor(time)))
