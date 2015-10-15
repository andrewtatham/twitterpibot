from ScheduledTask import ScheduledTask
from OutgoingTweet import OutgoingTweet
import random
import time
from apscheduler.triggers.cron import CronTrigger
import hardware
from TwitterHelper import Send

class PhotoScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger(hour = "*/3")


    def onRun(args):
        photos = hardware.TakePhotoToDisk("temp", "PhotoScheduledTask", "jpg")
        if any(photos):
            tweet = OutgoingTweet(filePaths=photos)
            Send(tweet)