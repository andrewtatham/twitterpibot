
from Task import Task
from InboxItemFactory import InboxItemFactory
from ResponseFactory import ResponseFactory



class ProcessInboxTask(Task):
    def onInit(args):
        args.factory = InboxItemFactory()
        args.responseFactory = ResponseFactory(context = args.context)
    

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

        args.context.piglow.OnInboxItemRecieved(inboxItem=inboxItem)

        # determine response
        response = args.responseFactory.Create(inboxItem)


        if response :

            #todo uploads
            args.context.outbox.put(response)
            



                    
            
            

