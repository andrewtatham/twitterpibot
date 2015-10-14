
from Task import Task
import time
import hardware
class FadeTask(Task):
    def onRun(args):
        hardware.Fade()
        time.sleep(1)
