import abc
import datetime
import logging

from twitterpibot import tasks
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask

logger = logging.getLogger(__name__)


class StreamingTopicScheduledTask(ScheduledTask):
    def __init__(self, identity, task_key):
        super(StreamingTopicScheduledTask, self).__init__(identity)
        self._streaming = False
        self._task_key = task_key

    def on_run(self):
        self._manage_topic_stream()

    @abc.abstractmethod
    def _get_topic_streamer(self):
        return None

    @abc.abstractmethod
    def _should_stream(self, today):
        return False

    def _manage_topic_stream(self):
        should_stream = self._should_stream(today=datetime.date.today())
        start = should_stream and not self._streaming
        stop = not should_stream and self._streaming
        if start:
            self._start_topic_stream()
        if stop:
            self._stop_topic_stream()

    def _start_topic_stream(self):
        logger.info("starting stream %s", self._task_key)
        streamer = self._get_topic_streamer()
        if streamer:
            task = StreamTweetsTask(identity=self.identity, streamer=streamer, key=self._task_key)
            tasks.add(task)
            self._streaming = True

    def _stop_topic_stream(self):
        logger.info("stopping stream %s", self._task_key)
        tasks.remove(self._task_key)
        self._streaming = False
