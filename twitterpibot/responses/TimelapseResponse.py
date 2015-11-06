from twitterpibot.responses.Response import Response
from twitterpibot.processing.Timelapse import Timelapse
import datetime
from twitterpibot.schedule import MySchedule


class TimelapseResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.isDirectMessage and not inbox_item.from_me and inbox_item.to_me \
               and "timelapse" in inbox_item.words

    def respond(self, inbox_item):
        now = datetime.datetime.now()
        timelapse = Timelapse(
            name='now',
            startTime=now + datetime.timedelta(seconds=1),
            endTime=now + datetime.timedelta(minutes=2),
            intervalSeconds=30,
            tweetText="")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            MySchedule.add(task)
