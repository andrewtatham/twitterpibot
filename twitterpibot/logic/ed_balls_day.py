import datetime
import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic import imagemanager
from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse
from twitterpibot.schedule.StreamTopicScheduledTask import StreamingTopicScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

link = "https://twitter.com/edballs/status/63623585020915713"


class TweetEdBallsDayScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(month=4, day=28, hour=16, minute=20, second="*/5")

    def on_run(self):
        text = ""
        r = random.randint(0, 1)
        if r == 0:
            text += "Happy ED BALLS day!"
        else:
            text = "ED BALLS"

        text += " #EdBallsDay"

        text += datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")

        if random.randint(0, 1):
            text += datetime.datetime.now().strftime(" #EdBallsDay%Y")

        file_path = imagemanager.get_ed_balls_image()
        file_paths = None
        if file_path:
            file_paths = [file_path]

        quote = None
        if random.randint(0, 1):
            quote = link


        print(text, quote, file_paths)
        # self.identity.twitter.send(OutgoingTweet(text=text, file_paths=file_paths, quote=quote))


class StreamEdBallsDayScheduledTask(StreamingTopicScheduledTask):
    def __init__(self, identity):
        super(StreamEdBallsDayScheduledTask, self).__init__(identity=identity, task_key="#EdBallsDay")

    def get_trigger(self):
        return CronTrigger(month=4, day="27-29", minute="*/2")

    def _get_topic_streamer(self):
        return self.identity.twitter.get_streamer(
            topic="Ed Balls,#EdBallsDay",
            topic_name=self._task_key,
            responses=[FavoriteResponse(self.identity), RetweetResponse(self.identity)],
            filter_level="low"
        )

    def _should_stream(self, today):
        return today.month == 4 and today.day == 28

if __name__ == '__main__':
    import identities
    identity = identities.AndrewTathamPi2Identity()
    task = TweetEdBallsDayScheduledTask(identity)
    for _ in range(100):
        task.on_run()
