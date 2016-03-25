import astral
import datetime
import logging

logger = logging.getLogger(__name__)


def get_today_times():
    a = astral.Astral()
    city = a['Leeds']
    sun = city.sun(date=datetime.date.today(), local=True)

    logger.info("[Astral] dawn: " + str(sun['dawn']))
    logger.info("[Astral] sunrise: " + str(sun['sunrise']))
    logger.info("[Astral] noon: " + str(sun['noon']))
    logger.info("[Astral] sunset: " + str(sun['sunset']))
    logger.info("[Astral] dusk: " + str(sun['dusk']))
    return sun


def get_tomorrow_times():
    a = astral.Astral()
    city = a['Leeds']
    sun = city.sun(date=datetime.date.today() + datetime.timedelta(days=1), local=True)

    logger.info("[Astral] dawn: " + str(sun['dawn']))
    logger.info("[Astral] sunrise: " + str(sun['sunrise']))
    logger.info("[Astral] noon: " + str(sun['noon']))
    logger.info("[Astral] sunset: " + str(sun['sunset']))
    logger.info("[Astral] dusk: " + str(sun['dusk']))

    return sun


class MyAstral(object):
    pass
