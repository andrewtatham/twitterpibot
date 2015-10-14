from Task import Task
import TwitterHelper
import Identity

class StreamTweetsTask(Task):
    def __init__(self, streamer):
        self.streamer = streamer
 
    def onRun(args):
        print("starting stream")
        args.streamer.user()

    def onStop(args):
        print("stopping stream")
        args.streamer.disconnect()






