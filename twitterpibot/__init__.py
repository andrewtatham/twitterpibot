import logging

import colorama
import twitterpibot.hardware
import twitterpibot.identities
import twitterpibot.responses
import twitterpibot.schedule
import twitterpibot.tasks
import twitterpibot.MyLogging

logger = logging.getLogger(__name__)

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)


def start():
    logger.info("Starting")
    twitterpibot.tasks.set_tasks(twitterpibot.identities.get_all_tasks())
    twitterpibot.schedule.set_scheduled_jobs(twitterpibot.identities.get_all_scheduled_jobs())
    twitterpibot.tasks.start()
    twitterpibot.schedule.start()
    logger.info("Started")


def stop():
    logger.info("Stopping")
    twitterpibot.schedule.stop()
    twitterpibot.tasks.stop()
    twitterpibot.hardware.stop()
    logger.info("Stopped")
