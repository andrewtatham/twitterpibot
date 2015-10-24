from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
import datetime
from colorama import Style, Fore
import os
import twitterpibot.MyQueues as MyQueues
import psutil


class MonitorScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(minute='*/5')

    def onRun(self):
        text = datetime.datetime.now().strftime("%c")
        text += os.linesep + 'cpu = ' + str(psutil.cpu_percent()) + ' memory = ' + str(psutil.virtual_memory().percent)
        text += os.linesep + 'inbox = ' + str(MyQueues.inbox.qsize())

        print(Style.BRIGHT + Fore.BLUE + text)
