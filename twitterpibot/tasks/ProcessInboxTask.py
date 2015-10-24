from twitterpibot.responses.ResponseFactory import ResponseFactory
from twitterpibot.tasks.Task import Task
from twitterpibot.incoming.InboxItemFactory  import InboxItemFactory
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
                inbox_item = self.factory.Create(data)
                if inbox_item:
                    if type(inbox_item) is IncomingTweet:
                        RecordIncomingTweet()
                    if type(inbox_item) is IncomingDirectMessage:
                        RecordIncomingDirectMessage()
                    Processinbox_item(self, inbox_item)
        finally:
            twitterpibot.MyQueues.inbox.task_done()

    def onStop(self):
        twitterpibot.MyQueues.inbox.put(None)


def Processinbox_item(args, inbox_item):
    inbox_item.Display()

    hardware.Oninbox_itemRecieved(inbox_item)

    response = args.responseFactory.Create(inbox_item)
    if response:
        Send(response)
