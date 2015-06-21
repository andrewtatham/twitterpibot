from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from OutgoingTweet import OutgoingTweet
import random
class PhotoScheduledTask(ScheduledTask):

    def  __init__(self, *args, **kwargs):

        self.messages = ["cheese!", "smile!"]


        return super(PhotoScheduledTask, self).__init__(*args, **kwargs)

    def GetTrigger(args):
        return IntervalTrigger(minutes=7)


    def onRun(args):

        args.context.piglow.CameraFlash(True)

        photos = args.context.cameras.TakePhotos()

        args.context.piglow.CameraFlash(False)

        media_ids = args.context.UploadMedia(photos)

        text = random.choice(args.messages)



        tweet = OutgoingTweet(text=text,media_ids=media_ids)
        args.Context.outbox.add(tweet)