from multiprocessing import Lock
import os
import datetime
class Statistics(object):
    def __init__(self, *args, **kwargs):
        self.lock = Lock()
        self.Reset()
        
    def Reset(args):
        with args.lock:
            args.IncomingTweets = 0
            args.IncomingDirectMessages = 0
            args.OutgoingTweets = 0
            args.OutgoingDirectMessages = 0
            args.Warnings = 0
            args.Errors = 0

    def GetStatistics(args):
        text = "Stats at " + datetime.datetime.now().strftime("%x %X") + os.linesep
            
        with args.lock:
            text += str(args.IncomingTweets) + " IncomingTweets" + os.linesep
            text += str(args.IncomingDirectMessages) + " IncomingDirectMessages" + os.linesep
            text += str(args.OutgoingTweets) + " OutgoingTweets: " + os.linesep
            text += str(args.OutgoingDirectMessages) + " OutgoingDirectMessages" +  os.linesep
            text += str(args.Warnings) + " Warnings" + os.linesep
            text += str(args.Errors) + " Errors" + os.linesep

        return text

    def RecordIncomingTweet(args):
        with args.lock:
            args.IncomingTweets += 1

    def RecordIncomingDirectMessage(args):
        with args.lock:
            args.IncomingDirectMessages += 1

    def RecordOutgoingTweet(args):
        with args.lock:
            args.OutgoingTweets += 1

    def RecordOutgoingDirectMessage(args):
        with args.lock:
            args.OutgoingDirectMessages += 1

    def RecordWarning(args):
        with args.lock:
            args.Warnings += 1

    def RecordError(args):
        with args.lock:
            args.Errors += 1
