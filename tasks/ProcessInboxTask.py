
from Task import Task
from InboxItemFactory import InboxItemFactory



class ProcessInboxTask(Task):
    def onInit(args):
        print('onInit')
        args.factory = InboxItemFactory()
    

    def onRun(args):
        print('processing inbox')
        data = args.Context.inbox.get()
        inboxItem = args.factory.Create(data)
        if inboxItem is not None:
            ProcessInboxItem(inboxItem)
        args.Context.inbox.task_done()

    def onStop(args):
        print('onStop')




def ProcessInboxItem(inboxItem):

      
        #todo downloads

        # show items
        inboxItem.Display()
        # determine response


        #todo uploads


        # todo send

        #if inboxItem.NeedsRely():
        #    inboxItem.Reply()

                    
            
            

