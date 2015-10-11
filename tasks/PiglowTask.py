
from Task import Task
import time
import sys
class PiglowTask(Task):
    def onRun(args):
        if piglow:
            piglow.Fade()
        time.sleep(1)
