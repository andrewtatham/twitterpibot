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
    Retweets = 0
    Favourites = 0


def reset():
    with _statsLock:
        global IncomingTweets
        global IncomingDirectMessages
        global OutgoingTweets
        global OutgoingDirectMessages
        global Warnings
        global Errors
        global Retweets
        global Favourites

        IncomingTweets = 0
        IncomingDirectMessages = 0
        OutgoingTweets = 0
        OutgoingDirectMessages = 0
        Warnings = 0
        Errors = 0
        Retweets = 0
        Favourites = 0


def get_statistics():
    text = "Stats at " + datetime.datetime.now().strftime("%x %X") + os.linesep

    with _statsLock:
        global IncomingTweets
        global IncomingDirectMessages
        global OutgoingTweets
        global OutgoingDirectMessages
        global Warnings
        global Errors
        global Retweets
        global Favourites

        text += str(IncomingTweets) + " IncomingTweets" + os.linesep
        text += str(IncomingDirectMessages) + " IncomingDirectMessages" + os.linesep
        text += str(OutgoingTweets) + " OutgoingTweets: " + os.linesep
        text += str(OutgoingDirectMessages) + " OutgoingDirectMessages" + os.linesep
        text += str(Warnings) + " Warnings" + os.linesep
        text += str(Errors) + " Errors" + os.linesep
        text += str(Retweets) + " Retweets" + os.linesep
        text += str(Favourites) + " Favourites" + os.linesep

    return text


def record_incoming_tweet():
    with _statsLock:
        global IncomingTweets
        IncomingTweets += 1


def record_incoming_direct_message():
    with _statsLock:
        global IncomingDirectMessages
        IncomingDirectMessages += 1


def record_outgoing_tweet():
    with _statsLock:
        global OutgoingTweets
        OutgoingTweets += 1


def record_outgoing_direct_message():
    with _statsLock:
        global OutgoingDirectMessages
        OutgoingDirectMessages += 1


def record_warning():
    with _statsLock:
        global Warnings
        Warnings += 1


def record_error():
    with _statsLock:
        global Errors
        Errors += 1


def record_retweet():
    with _statsLock:
        global Retweets
        Retweets += 1


def record_favourite():
    with _statsLock:
        global Favourites
        Favourites += 1
