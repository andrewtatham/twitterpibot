import datetime
import logging
import re

from apscheduler.triggers.cron import CronTrigger

from twitterpibot import tasks
from twitterpibot.responses.Response import Response
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask

logger = logging.getLogger(__name__)


def _is_iwd(today=None):
    if not today:
        today = datetime.date.today()
    return today.month == 3 and today.day == 8


class InternationalWomensDayScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(InternationalWomensDayScheduledTask, self).__init__(identity)
        self._streaming = False

    def get_trigger(self):
        return CronTrigger(month=3, day="7-9", minute="*/5")

    def on_run(self):
        task_key = "#InternationalWomensDay"
        is_iwd = _is_iwd()
        start = is_iwd and not self._streaming
        stop = not is_iwd and self._streaming
        if start:
            logger.info("starting stream %s", task_key)
            responses = [InternationalWomensDayResponse(self.identity)]

            streamer = self.identity.twitter.get_streamer(
                topic="international men day," +
                      "#meninist,#InternationalMensDay," +
                      "#InternationalWomenDay,#InternationalWomensDay",
                topic_name="#InternationalWomensDay",
                responses=responses)
            task = StreamTweetsTask(identity=self.identity, streamer=streamer, key=task_key)
            tasks.add(task)
            self._streaming = True

        if stop:
            logger.info("stopping stream %s", task_key)
            tasks.remove(task_key)
            self._streaming = False


class InternationalWomensDayResponse(Response):
    def __init__(self, identity):
        super(InternationalWomensDayResponse, self).__init__(identity)
        self._question_rx = re.compile("(When|is.*there|(how|what).*about).*international.*men'?s.*day\?", flags=re.IGNORECASE)

        self._answer_rx_1 = re.compile("19|nineteen", flags=re.IGNORECASE)
        self._answer_rx_2 = re.compile("Nov", flags=re.IGNORECASE)

    def condition(self, inbox_item):
        return (inbox_item.is_tweet or inbox_item.is_direct_message) \
               and bool(self._question_rx.findall(inbox_item.text)) \
               and not (
                bool(self._answer_rx_1.findall(inbox_item.text)) and bool(self._answer_rx_2.findall(inbox_item.text)))

    def respond(self, inbox_item):
        self.identity.twitter.reply_with(
            inbox_item,
            text="International Mens Day is on November 19th #InternationalWomensDay")
