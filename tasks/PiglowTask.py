
from Task import Task
import time
import hardware
class PiglowTask(Task):
    def onRun(args):

        hardware.piglow.Fade()
        time.sleep(1)
