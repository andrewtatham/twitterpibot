from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
import datetime
from colorama import Style, Fore
import os
import twitterpibot.MyQueues as MyQueues
import psutil
from twitterpibot.tasks import Tasks
import logging
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
