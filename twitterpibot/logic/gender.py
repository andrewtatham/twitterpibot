import logging
import random
import re

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic.phrase_generator import generate_phrase
from twitterpibot.responses.Response import Response
from twitterpibot.schedule.StreamTopicScheduledTask import StreamingTopicScheduledTask

logger = logging.getLogger(__name__)

_question_rx = re.compile(
    pattern=
    "(What|When|Why|Where|is there|how about|what about|isn't|We want|Do we need|There is no|backlash|outcry)"
    ".*"
    "(#InternationalMensDay|((inter)?national)?.*men'?s?.*day)"
    ".*"
    "(\\?)?"  # literal question mark, optional
    ,
    flags=re.IGNORECASE)

_answer = re.compile(
    "(19|nineteen"
    "|11|Nov"
    "|Every( ?| single | other )day"
    "|364|365"
    "|ask"
    "|insecure"
    "|@Herring1967"
    "|Richard Herring"
    "|Day\?? Day)"
    , flags=re.IGNORECASE)


def is_question(text):
    return _question_rx.findall(text)


def is_answer(text):
    return _answer.findall(text)


# responses
# @UKMensDay
# @Herring1967

# Let me google that for you http://lmgtfy.com/?q=When+is+international+mens+day

# Make a donation to https://www.justgiving.com/fundraising/November19th?

responses = [
    "(International Men's Day|#InternationalMensDay) is on (the 19th of November|November 19th|19th Nov)."
]

_lol = re.compile("lol", flags=re.IGNORECASE)
_sexist = re.compile("(sexis(t|m))", flags=re.IGNORECASE)
_swear = re.compile("fuck|bitches", flags=re.IGNORECASE)

def is_lol(text):
    return _lol.findall(text)
def is_sexist(text):
    return _sexist.findall(text)
def is_swear(text):
    return _swear.findall(text)
def get_response(text):
    response = generate_phrase(responses)
    if is_lol(text):
        response += " lol"
    sexist = is_sexist(text)
    if sexist:
        print(sexist)
        sexist_text = str(sexist.text)
        response += " #Not".format(sexist_text)
    if is_swear(text):
        response += " #WashYourMouth"
    return response


class WhenIsIMDScheduledTask(StreamingTopicScheduledTask):
    def __init__(self, identity):
        super(WhenIsIMDScheduledTask, self).__init__(identity, task_key="#InternationalWomensDay")

    def get_trigger(self):
        return CronTrigger(month=3, day="7-9", minute="*/5")

    def _should_stream(self, today):
        return today.month == 3 and today.day == 8

    def _get_topic_streamer(self):
        return self.identity.twitter.get_streamer(
            topic="men day",
            topic_name=self._task_key,
            responses=[WhenIsInternationalMensDayResponse(self.identity)],
            filter_level="none"
        )


class WhenIsInternationalMensDayResponse(Response):
    def __init__(self, identity):
        super(WhenIsInternationalMensDayResponse, self).__init__(identity)

    def condition(self, inbox_item):
        return (inbox_item.is_tweet or inbox_item.is_direct_message) \
               and bool(is_question(inbox_item.text)) \
               and not (is_answer(inbox_item.text))

    def respond(self, inbox_item):
        self.identity.statistics.increment("International womens/mens day tweets")

        response = get_response(inbox_item.text)

        if random.randint(0, 3) == 0:
            self.identity.twitter.reply_with(inbox_item, text=response)
        else:
            self.identity.twitter.quote_tweet(inbox_item, text=response)


if __name__ == '__main__':
    for _ in range(10):
        print(get_response(""))
