from twitterpibot.incoming.InboxItem import InboxItem
from twitterpibot.responses.Response import Response
from twitterpibot.processing.Timelapse import Timelapse
import datetime
from twitterpibot.schedule import MySchedule


class TimelapseResponse(Response):
    def condition(self, inbox_item:InboxItem):
        return inbox_item.is_direct_message and not inbox_item.from_me and inbox_item.to_me \
               and "timelapse" in inbox_item.words

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
