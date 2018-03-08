import logging
import random
import re

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.responses.Response import Response
from twitterpibot.schedule.StreamTopicScheduledTask import StreamingTopicScheduledTask

logger = logging.getLogger(__name__)

_question_rx = re.compile(
    pattern="When|is.*there|(how|what).*about|Why.*(no|isn't)|We want|Do we need|There is no|Where|What|backlash|outcry"
            ".*"
            "(inter)?national"
            ".*"
            "men'?s.*day"
            ".*"
            "\??" # literal question mark, optional
    ,
    flags=re.IGNORECASE)

_answer_rx_1 = re.compile(
    "(19|nineteen)|(11|Nov)"
      "|Every( ?| single | other )day"
    "|364|365"
    "|ask"
    "|insecure"
    "|@Herring1967"
    , flags=re.IGNORECASE)


def is_question(text):
    return bool(_question_rx.findall(text))

def is_not_question(text):
    return bool(_answer_rx_1.findall(text))


# responses
# @UKMensDay
# @Herring1967

# Let me google that for you http://lmgtfy.com/?q=When+is+international+mens+day

# Make a donation to https://www.justgiving.com/fundraising/November19th?

responses = ["International Men's Day is on November 19th"]


class WhenIsIMDScheduledTask(StreamingTopicScheduledTask):
    def __init__(self, identity):
        super(WhenIsIMDScheduledTask, self).__init__(identity, task_key="#InternationalWomensDay")

    def get_trigger(self):
        return CronTrigger(month=3, day="7-9", minute="*/5")

    def _should_stream(self, today):
        return today.month == 3 and today.day == 8

    def _get_topic_streamer(self):
        return self.identity.twitter.get_streamer(
            topic="men,day",
            topic_name=self._task_key,
            responses=[WhenIsInternationalMensDayResponse(self.identity)],
            filter_level="none"
        )


class WhenIsInternationalMensDayResponse(Response):
    def __init__(self, identity):
        super(WhenIsInternationalMensDayResponse, self).__init__(identity)

    def condition(self, inbox_item):
        # when in quotes its rhetorical so ignore, also answers were sometimes images
        return (inbox_item.is_tweet or inbox_item.is_direct_message) \
               and is_question(inbox_item.text) \
               and not is_not_question(inbox_item.text)

    def respond(self, inbox_item):
        self.identity.statistics.increment("International womens/mens day tweets")
        response = random.choice(responses)

        self.identity.twitter.quote_tweet(
            inbox_item,
            text=response)
