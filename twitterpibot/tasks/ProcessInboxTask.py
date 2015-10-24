from twitterpibot.responses.ResponseFactory import ResponseFactory
from twitterpibot.tasks.Task import Task
from twitterpibot.incoming.InboxItemFactory import InboxItemFactory
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage
from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.Statistics import RecordIncomingTweet, RecordIncomingDirectMessage
from twitterpibot.twitter.TwitterHelper import Send

import twitterpibot.hardware.hardware as hardware
import twitterpibot.MyQueues


class ProcessInboxTask(Task):
    def __init__(self):
        self.factory = InboxItemFactory()
        self.responseFactory = ResponseFactory()

    def onRun(self):
        try:
            data = twitterpibot.MyQueues.inbox.get()
            if data:
                inboxItem = self.factory.Create(data)
                if inboxItem:
                    if type(inboxItem) is IncomingTweet:
                        RecordIncomingTweet()
                    if type(inboxItem) is IncomingDirectMessage:
                        RecordIncomingDirectMessage()
                    ProcessInboxItem(self, inboxItem)
        finally:
            twitterpibot.MyQueues.inbox.task_done()

    def onStop(self):
        twitterpibot.MyQueues.inbox.put(None)


def ProcessInboxItem(args, inboxItem):
    inboxItem.Display()

    hardware.OnInboxItemRecieved(inboxItem)

    response = args.responseFactory.Create(inboxItem)
    if response:
        Send(response)
