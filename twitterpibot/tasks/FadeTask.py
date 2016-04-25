from twitterpibot.hardware import myperipherals
from twitterpibot.tasks.Task import Task
import time


class FadeTask(Task):
    def __init__(self):
        Task.__init__(self, None)
        self.core = True

    def on_run(self):
        myperipherals.on_fade_task()
        time.sleep(1)
