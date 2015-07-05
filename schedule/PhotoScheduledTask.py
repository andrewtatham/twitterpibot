from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from OutgoingTweet import OutgoingTweet
import random
class PhotoScheduledTask(ScheduledTask):

    def  __init__(self, *args, **kwargs):

        return super(PhotoScheduledTask, self).__init__(*args, **kwargs)

    def GetTrigger(args):
        #return IntervalTrigger(seconds=15)
        #return IntervalTrigger(minutes=15)
        return IntervalTrigger(hours=3, minutes=15)


    def onRun(args):

        args.context.piglow.CameraFlash(True)

        photos = args.context.cameras.TakePhotos()

        args.context.piglow.CameraFlash(False)

        media_ids = args.context.UploadMedia(photos)



        if any(media_ids):
            tweet = OutgoingTweet(media_ids=media_ids)
            args.context.outbox.put(tweet)