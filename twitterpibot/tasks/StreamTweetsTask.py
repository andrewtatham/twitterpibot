import logging

from twitterpibot.tasks.Task import Task

logger = logging.getLogger(__name__)


class StreamTweetsTask(Task):
    def __init__(self, identity, streamer=None, key=None):
        Task.__init__(self, identity, key=key)
        self.core = True
        if not streamer:
            self._streamer = identity.twitter.get_streamer()
        else:
            self._streamer = streamer

    def on_run(self):
        if self._streamer._topic:
            logger.info("starting %s %s topic stream", self.identity.screen_name, self._streamer._topic_name)
            self._streamer.statuses.filter(
                track=self._streamer._topic,
                filter_level=self._streamer._filter_level,
                language="en")
        else:
            logger.info("starting %s user stream" % self.identity.screen_name)
            self._streamer.user()

    def on_stop(self):
        logger.info("disconnecting %s stream" % self.identity.screen_name)
        self._streamer.disconnect()
