import logging
import random
import re

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.responses.Response import Response
from twitterpibot.schedule.StreamTopicScheduledTask import StreamingTopicScheduledTask

logger = logging.getLogger(__name__)


class WhenIsIMDScheduledTask(StreamingTopicScheduledTask):
    def __init__(self, identity):
        super(WhenIsIMDScheduledTask, self).__init__(identity, task_key="#InternationalWomensDay")

    def get_trigger(self):
        return CronTrigger(month=3, day="7-9", minute="*/5")

    def _should_stream(self, today):
        return today.month == 3 and today.day == 8

    def _get_topic_streamer(self):
        return self.identity.twitter.get_streamer(
            topic="international men day",
            topic_name=self._task_key,
            responses=[WhenIsInternationalMensDayResponse(self.identity)],
            filter_level="none"
        )


responses = ["International Men's Day is on November 19th"]


class WhenIsInternationalMensDayResponse(Response):
    def __init__(self, identity):
        super(WhenIsInternationalMensDayResponse, self).__init__(identity)
        self._question_rx = re.compile(
            pattern="(When|is.*there|(how|what).*about).*international.*men'?s.*day\?",
            flags=re.IGNORECASE)

        self._answer_rx_1 = re.compile("19|nineteen", flags=re.IGNORECASE)
        self._answer_rx_2 = re.compile("11|Nov", flags=re.IGNORECASE)

    def condition(self, inbox_item):
        # when in quotes its rhetorical so ignore, also answers were sometimes images
        return (inbox_item.is_tweet or inbox_item.is_direct_message) \
               and not inbox_item.has_media \
               and '"' not in inbox_item.text \
               and bool(self._question_rx.findall(inbox_item.text)) \
               and not (bool(self._answer_rx_1.findall(inbox_item.text))
                        and bool(self._answer_rx_2.findall(inbox_item.text)))

    def respond(self, inbox_item):
        self.identity.statistics.increment("International womens/mens day tweets")
        response = random.choice(responses)
        self.identity.twitter.quote_tweet(
            inbox_item,
            text=response)
