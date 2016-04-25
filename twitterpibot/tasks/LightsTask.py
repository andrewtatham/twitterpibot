from twitterpibot.tasks.Task import Task
from twitterpibot.hardware import myhardware


class LightsTask(Task):
    def __init__(self):
        Task.__init__(self, None)
        self.core = True

    def on_run(self):
        myhardware.on_lights_task()
