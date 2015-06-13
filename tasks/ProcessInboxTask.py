
from Task import Task
from InboxItemFactory import InboxItemFactory
from ResponseFactory import ResponseFactory



class ProcessInboxTask(Task):
    def onInit(args):
        args.factory = InboxItemFactory()
        args.responseFactory = ResponseFactory(context = args.Context)
    

    def onRun(args):
        data = args.Context.inbox.get()
        inboxItem = args.factory.Create(data)
        if inboxItem is not None:
            ProcessInboxItem(args, inboxItem)
        args.Context.inbox.task_done()



def ProcessInboxItem(args, inboxItem):

      
        #todo downloads

        # show items
        inboxItem.Display()

        # determine response
        response = args.responseFactory.Create(inboxItem)


        if response is not None:

            #todo uploads
            args.Context.outbox.put(response)
            



                    
            
            

