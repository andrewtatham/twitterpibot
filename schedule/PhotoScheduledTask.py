from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from OutgoingTweet import OutgoingTweet
import random
import time
from apscheduler.triggers.cron import CronTrigger
class PhotoScheduledTask(ScheduledTask):

    def  __init__(self, *args, **kwargs):

        return super(PhotoScheduledTask, self).__init__(*args, **kwargs)

    def GetTrigger(args):

        return CronTrigger(hour='8-22', minute='*/20')


    def onRun(args):

        args.context.CameraFlash(True)
        time.sleep(1)
        photos = args.context.cameras.TakePhotos()

        args.context.CameraFlash(False)

        media_ids = args.context.UploadMedia(photos)



        if any(media_ids):
            tweet = OutgoingTweet(media_ids=media_ids)
            args.context.outbox.put(tweet)