from twitterpibot.tasks.Task import Task


class StreamTweetsTask(Task):
    def __init__(self, streamer, topic=None):
        Task.__init__(self)
        self._streamer = streamer
        self._topic = topic
        if self._topic:
            self.key = self._topic
        else:
            self.core = True

    def onRun(self):
        if self._topic:
            print("starting topic stream = " + self._topic)
            self._streamer.statuses.filter(track=self._topic)
        else:
            print("starting user stream")
            self._streamer.user()

    def onStop(self):
        if self._topic:
            print("stopping topic stream = " + self._topic)
        else:
            print("stopping user stream")
        self._streamer.disconnect()
