from twitterpibot.tasks.Task import Task
import twitterpibot.hardware.hardware as hardware


class LightsTask(Task):
    def __init__(self):
        Task.__init__(self)
        self.core = True

    def on_run(self):
        hardware.on_lights_task()
