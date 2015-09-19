
from Task import Task
from InboxItemFactory import InboxItemFactory
from ResponseFactory import ResponseFactory
import sys



class ProcessInboxTask(Task):

    def onInit(args):
        args.factory = InboxItemFactory(args.context)
        args.responseFactory = ResponseFactory(args.context)
    

    def onRun(args):
        try:
            data = args.context.inbox.get()
            if data:
                inboxItem = args.factory.Create(data)
                if inboxItem :
                    ProcessInboxItem(args, inboxItem)
        finally:
            args.context.inbox.task_done()

    def onStop(args):
        args.context.inbox.put(None)

def ProcessInboxItem(args, inboxItem):
        inboxItem.Display()
        args.context.OnInboxItemRecieved(inboxItem=inboxItem)
        response = args.responseFactory.Create(inboxItem)
        if response :
            args.context.outbox.put(response)
            



                    
            
            

