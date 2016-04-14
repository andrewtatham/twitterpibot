from apscheduler.triggers.cron import CronTrigger
from colorama import Style, Fore
import psutil
import logging

from twitterpibot.schedule.ScheduledTask import ScheduledTask

__author__ = 'andrewtatham'

logger = logging.getLogger(__name__)


class GlobalMonitorScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute='*/20')

    def on_run(self):
        cpu = str(psutil.cpu_percent())
        mem = str(psutil.virtual_memory().percent)
        text = 'cpu = ' + cpu + ' memory = ' + mem
        logger.info(Style.BRIGHT + Fore.BLUE + text)
