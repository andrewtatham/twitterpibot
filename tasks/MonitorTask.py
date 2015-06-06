from Task import Task
import time

class MonitorTask(Task):
    def onRun(args):

        print(args.Context.GetStatus())

        time.sleep(1)

  