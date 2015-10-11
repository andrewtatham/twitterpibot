
from Task import Task
from InboxItemFactory import InboxItemFactory
from ResponseFactory import ResponseFactory
import sys
from IncomingDirectMessage import IncomingDirectMessage
from IncomingTweet import IncomingTweet
from Statistics import RecordIncomingTweet, RecordIncomingDirectMessage
from TwitterHelper import Send

global hardware


class ProcessInboxTask(Task):

    def onInit(args):
        args.factory = InboxItemFactory()
        args.responseFactory = ResponseFactory()
    

    def onRun(args):
        global inbox
        try:
            data = inbox.get()
            if data:
                inboxItem = args.factory.Create(data)
                if inboxItem :
                    if type(inboxItem) is IncomingTweet:
                        RecordIncomingTweet()
                    if type(inboxItem) is IncomingDirectMessage:
                        RecordIncomingDirectMessage()
                    ProcessInboxItem(args, inboxItem)
        finally:
            inbox.task_done()

    def onStop(args):
        inbox.put(None)

def ProcessInboxItem(args, inboxItem):
        inboxItem.Display()

        if hardware.piglowattached:
            piglow.OnInboxItemRecieved(inboxItem)

        response = args.responseFactory.Create(inboxItem)
        if response :
            Send(response)
            



                    
            
            

