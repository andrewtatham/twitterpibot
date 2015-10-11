from ScheduledTask import ScheduledTask
from OutgoingTweet import OutgoingTweet
import random
import time
from apscheduler.triggers.cron import CronTrigger
class PhotoScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger(hour = "*/3")


    def onRun(args):

        CameraFlash(True)
        time.sleep(1)
        photos = cameras.TakePhotos()

        CameraFlash(False)




        if any(photos):
            tweet = OutgoingTweet(photos=photos)
            Send(tweet)