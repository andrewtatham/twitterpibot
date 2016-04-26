from twitterpibot.tasks.Task import Task
from twitterpibot.hardware import myperipherals


class LightsTask(Task):
    def __init__(self):
        Task.__init__(self, None)
        self.core = True

    def on_run(self):
        myperipherals.on_fade_task()
        myperipherals.on_lights_task()
