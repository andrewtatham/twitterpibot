import datetime

from twitterpibot.responses.Response import Response
from twitterpibot.processing.Timelapse import Timelapse
from twitterpibot.schedule import MySchedule


class TimelapseResponse(Response):
    def condition(self, inbox_item):
        return super(TimelapseResponse, self) \
               and inbox_item.words and "timelapse" in inbox_item.words

    def respond(self, inbox_item):
        now = datetime.datetime.now()
        timelapse = Timelapse(
            name='now',
            start_time=now + datetime.timedelta(seconds=1),
            end_time=now + datetime.timedelta(minutes=2),
            interval_seconds=30,
            tweet_text="")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            MySchedule.add(task)
