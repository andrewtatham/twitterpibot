from ScheduledTask import ScheduledTask
from OutgoingTweet import OutgoingTweet
import random
import time
from apscheduler.triggers.cron import CronTrigger
import hardware

class PhotoScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger(hour = "*/3")


    def onRun(args):
        photos = hardware.TakePhotos()
        if any(photos):
            tweet = OutgoingTweet(photos=photos)
            Send(tweet)