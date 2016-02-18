import logging

from twitterpibot.tasks.Task import Task

logger = logging.getLogger(__name__)


class StreamTweetsTask(Task):
    def __init__(self, identity):
        Task.__init__(self, identity)
        self.core = True
        self._streamer = identity.twitter.get_streamer()

    def on_run(self):
        logger.info("starting %s stream" % self.identity.screen_name)
        self._streamer.user()

    def on_stop(self):
        logger.info("disconnecting %s stream" % self.identity.screen_name)
        self._streamer.disconnect()
