from Task import Task
import time

class MonitorTask(Task):
    def onRun(args):


        status = args.context.GetStatus()
        if(status.inboxCount + status.songCount + status.outboxCount > 0):
            print('inbox = ' + str(status.inboxCount)
                  + 'songs = ' + str(status.songCount)
                  + 'outbox = ' + str(status.outboxCount))

        time.sleep(15)

  