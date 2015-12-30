import logging
from twitterpibot.tasks.Task import Task

logger = logging.getLogger(__name__)


class StreamTweetsTask(Task):
    def __init__(self, streamer, core=False):
        Task.__init__(self)
        self._streamer = streamer
        self._topic = streamer.topic
        if self._topic:
            self.key = self._topic
            self.core = core
        else:
            # user stream is a core task
            self.core = True

    def onRun(self):
        if self._topic:
            logger.info("starting topic stream = " + self._topic)
            self._streamer.statuses.filter(track=self._topic, filter_level="low", language="en")
        else:
            logger.info("starting user stream")
            self._streamer.user()

    def onStop(self):
        if self._topic:
            logger.info("stopping topic stream = " + self._topic)
        else:
            logger.info("stopping user stream")
        self._streamer.disconnect()
