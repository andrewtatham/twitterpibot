import logging

from apscheduler.triggers.cron import CronTrigger
from colorama import Style, Fore
import psutil

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class GlobalMonitorScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute='*/20')

    def on_run(self):
        cpu = str(psutil.cpu_percent())
        mem = str(psutil.virtual_memory().percent)
        text = 'cpu = ' + cpu + ' memory = ' + mem
        logger.info(Style.BRIGHT + Fore.BLUE + text)


class IdentityMonitorScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute='*/15')

    def on_run(self):
        self.identity.conversations.housekeep()
