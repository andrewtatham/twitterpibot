from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime
from colorama import Style, Fore
import logging

class MonitorScheduledTask(ScheduledTask):


    def GetTrigger(args):
        return CronTrigger(minute = '*/5')
    

    def onRun(args):
        text = datetime.datetime.now().strftime("%c")
        print(Style.BRIGHT + Fore.BLUE + text)
        logging.info(text)



