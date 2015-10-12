
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

    def onInit(args):
        args.factory = InboxItemFactory()
        args.responseFactory = ResponseFactory()
    

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

        if hardware.ispiglowattached:
            hardware.piglow.OnInboxItemRecieved(inboxItem)

        response = args.responseFactory.Create(inboxItem)
        if response :
            Send(response)
            



                    
            
            

