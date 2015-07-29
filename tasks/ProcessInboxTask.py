
from Task import Task
from InboxItemFactory import InboxItemFactory
from ResponseFactory import ResponseFactory



class ProcessInboxTask(Task):

    def onInit(args):
        args.factory = InboxItemFactory(args.context)
        args.responseFactory = ResponseFactory(args.context)
    

    def onRun(args):


        try:

            data = args.context.inbox.get()
            inboxItem = args.factory.Create(data)
            if inboxItem :
                ProcessInboxItem(args, inboxItem)
        finally:
            args.context.inbox.task_done()



def ProcessInboxItem(args, inboxItem):

      
        #todo downloads

        # show items
        inboxItem.Display()

        args.context.OnInboxItemRecieved(inboxItem=inboxItem)

        # determine response
        response = args.responseFactory.Create(inboxItem)


        if response :
   
            args.context.outbox.put(response)
            



                    
            
            

