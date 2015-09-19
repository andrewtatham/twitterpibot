
from Task import Task
import time
import sys
class PiglowTask(Task):
    def onRun(args):
        if args.context.piglow:
            args.context.piglow.Fade()
        time.sleep(1)
