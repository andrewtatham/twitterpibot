import logging
import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic import bbc_weather_bot
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class WeatherScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=random.randint(24, 48), minute=random.randint(0, 59))

    def on_run(self):
        tweet_id = self.identity.twitter.send(OutgoingTweet(text="@" + bbc_weather_bot.screen_name + " Leeds Today"))
        # todo track conversation?
        self.identity.conversations.track_replies(tweet_id=tweet_id, response=self.on_response)

    def on_response(self, inbox_item):
        pass

