from twitterpibot.tasks.Task import Task
import time
import twitterpibot.hardware.hardware as hardware


class FadeTask(Task):
    def __init__(self):
        Task.__init__(self) 
        self.core = True

    def onRun(self):
        hardware.on_fade_task()
        time.sleep(1)
