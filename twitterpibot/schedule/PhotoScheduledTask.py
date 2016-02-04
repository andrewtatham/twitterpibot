from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
import twitterpibot.hardware.hardware as hardware
from twitterpibot.twitter.TwitterHelper import send


class PhotoScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour="8-22", minute="*/20")

    def on_run(self):
        photos = hardware.take_photo("temp", "PhotoScheduledTask", "jpg")
        if any(photos):
            send(OutgoingTweet(file_paths=photos))
