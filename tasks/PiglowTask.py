
from Task import Task
import time
import hardware
class PiglowTask(Task):
    def onRun(args):

        if hardware.isunicornhatattached:
            hardware.unicornhat.Fade()
        if hardware.ispiglowattached:
            hardware.piglow.Fade()
        time.sleep(1)
