import datetime
import logging

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.tasks import Tasks
from twitterpibot.twitter import TwitterHelper, TrendingTopics
from twitterpibot.twitter.TwitterHelper import Send

logger = logging.getLogger(__name__)

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
                    logger.info("adding " + trend + " to stop list")
                    _stop_list.append(trend)

        if _trends_list:
            trend = _trends_list.pop()

            logger.info("checking " + trend)
            is_streaming = trend in stream_list
            if is_streaming:
                logger.info("adding " + trend + " to stop list")
                _stop_list.append(trend)
            else:
                logger.info("adding " + trend + " to start list")
                _start_list.append(trend)

        if _stop_list:
            text = "Stopping streams:"
            while _stop_list:
                stop_trend = _stop_list.pop()
                # stop stream
                text += " " + stop_trend
                Tasks.remove(stop_trend)
            logger.info(text)
            text += " at " + str(datetime.datetime.now())
            Send(OutgoingDirectMessage(text=text))
        elif _start_list:
            # Create stream
            start_trend = _start_list.pop()
            text = "Starting stream " + start_trend + " " + str(datetime.datetime.now())
            logger.info(text)
            Tasks.add(StreamTweetsTask(TwitterHelper.GetStreamer(topic=start_trend)))
            Send(OutgoingDirectMessage(text=text))
