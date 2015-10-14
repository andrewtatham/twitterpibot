
from Task import Task
from InboxItemFactory import InboxItemFactory
from ResponseFactory import ResponseFactory
from IncomingDirectMessage import IncomingDirectMessage
from IncomingTweet import IncomingTweet
from Statistics import RecordIncomingTweet, RecordIncomingDirectMessage
from TwitterHelper import Send

import hardware
import MyQueues

class ProcessInboxTask(Task):
    def __init__(self, *args, **kwargs):
        self.factory = InboxItemFactory()
        self.responseFactory = ResponseFactory()

    def onRun(args):
        try:
            data = MyQueues.inbox.get()
            if data:
                inboxItem = args.factory.Create(data)
                if inboxItem :
                    if type(inboxItem) is IncomingTweet:
                        RecordIncomingTweet()
                    if type(inboxItem) is IncomingDirectMessage:
                        RecordIncomingDirectMessage()
                    ProcessInboxItem(args, inboxItem)
        finally:
            MyQueues.inbox.task_done()

    def onStop(args):
        MyQueues.inbox.put(None)

def ProcessInboxItem(args, inboxItem):
        inboxItem.Display()

        hardware.OnInboxItemRecieved(inboxItem)

        response = args.responseFactory.Create(inboxItem)
        if response:
            Send(response)
            



                    
            
            

