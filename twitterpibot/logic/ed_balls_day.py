import datetime
import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic import imagemanager
from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse
from twitterpibot.schedule.StreamTopicScheduledTask import StreamingTopicScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

the_big_bang = "https://twitter.com/edballs/status/63623585020915713"
days_before = {1, 2, 3, 7, 14, 21, 25, 50, 100, 150, 200, 250, 300, 350, 364}


class TweetBeforeEdBallsDayScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=16, minute=20)

    def on_run(self):

        today = datetime.date.today()
        y = today.year
        m = today.month
        d = today.day

        is_ed_balls_day = d == 28 and m == 4
        if not is_ed_balls_day:
            is_ebd_next_year = m == 4 and d > 28 or m > 4
            if is_ebd_next_year:
                y += 1
            next_ed_balls_day = datetime.date(y, 4, 28)
            days_until_ebd = (next_ed_balls_day - datetime.date.today()).days

            if days_until_ebd in days_before:
                if days_until_ebd == 1:
                    text = random.choice(["GAAAH", "OMG", "ZOMG"])
                    text += " #EdBallsDay is "
                    text += random.choice(["nearly here", "so close"])
                else:
                    text = random.choice(["Only", "Just"])
                    text += " {} days until #EdBallsDay".format(days_until_ebd)
                text += "!" * random.randint(1, 7)

                file_path = imagemanager.get_ed_balls_image()
                file_paths = None
                if file_path:
                    file_paths = [file_path]

                if random.randint(0, 1):
                    text += " " + the_big_bang

                self.identity.twitter.send(OutgoingTweet(text=text, file_paths=file_paths))


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
            quote = the_big_bang

        self.identity.twitter.send(OutgoingTweet(text=text, file_paths=file_paths, quote=quote))


class StreamEdBallsDayScheduledTask(StreamingTopicScheduledTask):
    def __init__(self, identity):
        super(StreamEdBallsDayScheduledTask, self).__init__(identity=identity, task_key="#EdBallsDay")

    def get_trigger(self):
        return CronTrigger(month=4, day="27-29", minute="*/30")

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

    identity = identities.AndrewTathamIdentity()
    task = TweetBeforeEdBallsDayScheduledTask(identity)
    task.on_run()
