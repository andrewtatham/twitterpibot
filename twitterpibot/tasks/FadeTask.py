from twitterpibot.tasks.Task import Task
import time
import twitterpibot.hardware.hardware as hardware


class FadeTask(Task):
    def onRun(self):
        hardware.Fade()
        time.sleep(1)