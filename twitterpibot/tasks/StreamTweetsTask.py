from Task import Task
import TwitterHelper
import Identity

class StreamTweetsTask(Task):
    def __init__(self, streamer):
        self.streamer = streamer
 
    def onRun(self):
        print("starting stream")
        self.streamer.user()

    def onStop(self):
        print("stopping stream")
        self.streamer.disconnect()






