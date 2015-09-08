from ScheduledTask import ScheduledTask
from OutgoingTweet import OutgoingTweet
import random
import time
from apscheduler.triggers.cron import CronTrigger
class PhotoScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger("hours = */3")


    def onRun(args):

        args.context.CameraFlash(True)
        time.sleep(1)
        photos = args.context.cameras.TakePhotos()

        args.context.CameraFlash(False)




        if any(photos):
            tweet = OutgoingTweet(photos=photos)
            args.context.outbox.put(tweet)