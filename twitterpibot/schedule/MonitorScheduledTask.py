import datetime
import os
import logging

from apscheduler.triggers.cron import CronTrigger
from colorama import Style, Fore
import psutil

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class MonitorScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute='*/5')

    def on_run(self):
        text = datetime.datetime.now().strftime("%c")
        text += os.linesep + 'cpu = ' + str(psutil.cpu_percent()) \
                + ' memory = ' + str(psutil.virtual_memory().percent)
        text += os.linesep + self.identity.statistics.get_statistics()
        logger.info(Style.BRIGHT + Fore.BLUE + text)
