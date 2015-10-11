from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime
from colorama import Style, Fore
import logging
import os

class MonitorScheduledTask(ScheduledTask):


    def GetTrigger(args):
        return CronTrigger(minute = '*/5')
    

    def onRun(args):
        text = datetime.datetime.now().strftime("%c")
        text += os.linesep \
            + 'cpu = ' + str(psutil.cpu_percent()) \
            + ' memory = ' + str(psutil.virtual_memory().percent)  
        text += os.linesep \
                + 'inbox = ' + str(inbox.qsize())

        print(Style.BRIGHT + Fore.BLUE + text)
        logging.info(text)
