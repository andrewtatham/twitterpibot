from Authenticator import Authenticator
from twython.api import Twython
from MyStreamer import MyStreamer
from Task import Task
from MyTwitter import MyTwitter
import sys

class StreamTweetsTask(Task):

    def onInit(args):

        authenticator = Authenticator()
        tokens = authenticator.Authenticate()
                        
        args.streamer = MyStreamer(tokens[0],tokens[1],tokens[2],tokens[3])
        args.streamer.inbox = args.context.inbox
 
    def onRun(args):
        print("starting stream")
        args.streamer.user()

    def onStop(args):
        print("stopping stream")
        args.streamer.disconnect()





