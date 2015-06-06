
from Task import Task
from InboxItemFactory import InboxItemFactory



class ProcessInboxTask(Task):
    def onInit(args):
        args.factory = InboxItemFactory()
    

    def onRun(args):
        data = args.Context.inbox.get()
        inboxItem = factory.Create(data)
        if inboxItem is not None:
            ProcessInboxItem(inboxItem)
        args.Context.inbox.task_done()


def ProcessInboxItem(inboxItem):

      
        #todo downloads

        # show items
        inboxItem.Display()
        # determine response


        #todo uploads


        # todo send

        if inboxItem.NeedsRely():
            inboxItem.Reply()

                    
            
            

