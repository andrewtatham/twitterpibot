from twitterpibot.tasks.Task import Task
import twitterpibot.hardware.hardware as hardware


class LightsTask(Task):
    def __init__(self):
        Task.__init__(self)
        self.core = True

    def onRun(self):
        hardware.Lights()
