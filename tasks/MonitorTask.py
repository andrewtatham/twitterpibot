from Task import Task
import time

class MonitorTask(Task):
    def onRun(args):


        status = args.Context.GetStatus()
        if(status.inboxCount > 0):
            print('inbox = ' + str(status.inboxCount))

        time.sleep(1)

  