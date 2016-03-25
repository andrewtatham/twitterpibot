import datetime

from twitterpibot import schedule
from twitterpibot.responses.Response import Response, mentioned_reply_condition
from twitterpibot.logic.timelapses import Timelapse


class TimelapseResponse(Response):
    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item) \
               and inbox_item.words and "timelapse" in inbox_item.words

    def respond(self, inbox_item):
        now = datetime.datetime.now()
        timelapse = Timelapse(
            identity=self.identity,
            name='now',
            start_time=now + datetime.timedelta(seconds=1),
            end_time=now + datetime.timedelta(minutes=2),
            interval_seconds=30,
            tweet_text="")

        tasks = timelapse.get_scheduled_tasks()
        for task in tasks:
            schedule.add(task)
