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


        
        status = args.context.GetStatus()
        
        text += os.linesep + 'cpu = ' + str(status.cpu) \
            + ' memory = ' + str(status.memory)  


        if(status.inboxCount + status.songCount + status.outboxCount > 0):
            text += os.linesep + 'inbox = ' + str(status.inboxCount) \
                  + 'songs = ' + str(status.songCount) \
                  + 'outbox = ' + str(status.outboxCount)



        print(Style.BRIGHT + Fore.BLUE + text)
        logging.info(text)
