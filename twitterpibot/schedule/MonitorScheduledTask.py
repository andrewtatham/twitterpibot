import datetime
import os
import logging

from apscheduler.triggers.cron import CronTrigger
from colorama import Style, Fore
import psutil

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.tasks import Tasks

logger = logging.getLogger(__name__)

class MonitorScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(minute='*/5')

    def onRun(self):
        text = datetime.datetime.now().strftime("%c")
        text += os.linesep + 'cpu = ' + str(psutil.cpu_percent()) + ' memory = ' + str(psutil.virtual_memory().percent)
        tasks = Tasks.get()
        if tasks:
            for task in tasks:
                if task:
                    text += os.linesep + 'monitoring = ' + task

        logger.info(Style.BRIGHT + Fore.BLUE + text)
