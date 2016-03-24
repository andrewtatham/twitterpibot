import datetime

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse
from twitterpibot.schedule.StreamTopicScheduledTask import StreamingTopicScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class TweetEdBallsDayScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(month=4, day=28, hour=16, minute=20, second="*/5")

    def on_run(self):
        text = datetime.datetime.now().strftime("ED BALLS #EdBallsDay %d/%m/%Y %H:%M:%S #EdBallsDay%Y")
        tweet = OutgoingTweet(text=text)
        self.identity.twitter.send(tweet)


class StreamEdBallsDayScheduledTask(StreamingTopicScheduledTask):
    def __init__(self, identity):
        super(StreamEdBallsDayScheduledTask, self).__init__(identity=identity, task_key="#EdBallsDay")

    def get_trigger(self):
        return CronTrigger(month=4, day="27-29", minute="*/2")

    def _get_topic_streamer(self):
        return self.identity.twitter.get_streamer(
            topic="Ed Balls",
            topic_name=self._task_key,
            responses=[FavoriteResponse(self.identity), RetweetResponse(self.identity)],
            filter_level="none"
        )

    def _should_stream(self, today):
        return today.month == 4 and today.day == 28
