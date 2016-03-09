from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
import twitterpibot.hardware


class PhotoScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour="8-22", minute="*/20")

    def on_run(self):
        photos = twitterpibot.hardware.take_photo("temp", "PhotoScheduledTask", "jpg")
        if any(photos):
            self.identity.twitter.send(OutgoingTweet(file_paths=photos))
