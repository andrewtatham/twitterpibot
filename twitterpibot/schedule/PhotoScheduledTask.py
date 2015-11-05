from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
import twitterpibot.hardware.hardware as hardware
from twitterpibot.twitter.TwitterHelper import Send


class PhotoScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="*/3")

    def onRun(self):
        photos = hardware.take_photo("temp", "PhotoScheduledTask", "jpg")
        if any(photos):
            tweet = OutgoingTweet(filePaths=photos)
            Send(tweet)
