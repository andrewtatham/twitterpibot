from Response import Response
from twitterpibot.processing.Timelapse import Timelapse
import datetime
import MySchedule


class TimelapseResponse(Response):
    def Condition(self, inboxItem):
        return inboxItem.isDirectMessage and not inboxItem.from_me and inboxItem.to_me \
               and "timelapse" in inboxItem.words

    def Respond(self, inboxItem):
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
