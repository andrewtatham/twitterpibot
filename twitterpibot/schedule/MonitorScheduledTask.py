import datetime
import os
import logging

from apscheduler.triggers.cron import CronTrigger

from colorama import Style, Fore
import psutil

from twitterpibot import tasks
from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class GlobalMonitorScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute='*/5')

    def on_run(self):
        cpu = str(psutil.cpu_percent())
        mem = str(psutil.virtual_memory().percent)
        text = datetime.datetime.now().strftime("%c")
        text += os.linesep + 'cpu = ' + cpu + ' memory = ' + mem
        text += os.linesep + tasks.status()
        logger.info(Style.BRIGHT + Fore.BLUE + text)


class IdentityMonitorScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute='*/15')

    def on_run(self):
        text = datetime.datetime.now().strftime("%c")
        text += os.linesep + self.identity.statistics.get_statistics()
        logger.info(Style.BRIGHT + Fore.BLUE + text)
