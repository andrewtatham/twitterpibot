import datetime

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.tasks import Tasks
from twitterpibot.twitter import TwitterHelper, TrendingTopics
from twitterpibot.twitter.TwitterHelper import Send

_trends_list = []
_start_list = []
_stop_list = []


class StreamTrendsScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return IntervalTrigger(minutes=5)

    def onRun(self):
        global _trends_list
        global _start_list
        global _stop_list

        stream_list = Tasks.get()

        if not _trends_list:
            _trends_list.extend(TrendingTopics.get())

            # Check for streams that are no longer trending
            for trend in stream_list:
                is_trending = trend in _trends_list
                if not is_trending:
                    _stop_list.append(trend)

        if _trends_list:
            trend = _trends_list.pop()
            is_streaming = trend in stream_list
            if is_streaming:
                _stop_list.append(trend)
            else:
                _start_list.append(trend)

        if _stop_list:
            stop_trend = _stop_list.pop()
            # stop stream
            Send(OutgoingDirectMessage(text="Stopping stream " + stop_trend + " " + str(datetime.datetime.now())))
            Tasks.remove(stop_trend)

        if _start_list:
            # Create stream
            start_trend = _start_list.pop()
            Tasks.add(StreamTweetsTask(TwitterHelper.GetStreamer(topic=start_trend)))
            Send(OutgoingDirectMessage(text="Starting stream " + start_trend + " " + str(datetime.datetime.now())))
