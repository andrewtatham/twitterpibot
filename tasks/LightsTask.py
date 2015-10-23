
from Task import Task
import time
import hardware
class LightsTask(Task):
    def onRun(args):
        print("LightsTask")
        hardware.Lights()
