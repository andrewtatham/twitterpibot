from multiprocessing import Lock
import os
import datetime


_statsLock = Lock()
with _statsLock:
    IncomingTweets = 0
    IncomingDirectMessages = 0
    OutgoingTweets = 0
    OutgoingDirectMessages = 0
    Warnings = 0
    Errors = 0

        
def Reset():
    with _statsLock:
        global IncomingTweets
        global IncomingDirectMessages
        global OutgoingTweets
        global OutgoingDirectMessages
        global Warnings
        global Errors

        IncomingTweets = 0
        IncomingDirectMessages = 0
        OutgoingTweets = 0
        OutgoingDirectMessages = 0
        Warnings = 0
        Errors = 0

def GetStatistics():
    text = "Stats at " + datetime.datetime.now().strftime("%x %X") + os.linesep
            
    with _statsLock:
        global IncomingTweets
        global IncomingDirectMessages
        global OutgoingTweets
        global OutgoingDirectMessages
        global Warnings
        global Errors

        text += str(IncomingTweets) + " IncomingTweets" + os.linesep
        text += str(IncomingDirectMessages) + " IncomingDirectMessages" + os.linesep
        text += str(OutgoingTweets) + " OutgoingTweets: " + os.linesep
        text += str(OutgoingDirectMessages) + " OutgoingDirectMessages" +  os.linesep
        text += str(Warnings) + " Warnings" + os.linesep
        text += str(Errors) + " Errors" + os.linesep

    return text

def RecordIncomingTweet():
    with _statsLock:
        global IncomingTweets
        IncomingTweets += 1

def RecordIncomingDirectMessage():
    with _statsLock:
        global IncomingDirectMessages
        IncomingDirectMessages += 1

def RecordOutgoingTweet():
    with _statsLock:
        global OutgoingTweets
        OutgoingTweets += 1

def RecordOutgoingDirectMessage():
    with _statsLock:
        global OutgoingDirectMessages
        OutgoingDirectMessages += 1

def RecordWarning():
    with _statsLock:
        global Warnings
        Warnings += 1

def RecordError():
    with _statsLock:
        global Errors
        Errors += 1
