from twitterpibot.tasks.Task import Task
import twitterpibot.hardware.hardware as hardware


class LightsTask(Task):
    def onRun(self):
        hardware.Lights()
