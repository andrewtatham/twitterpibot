from twitterpibot.tasks.Task import Task
import twitterpibot.hardware


class LightsTask(Task):
    def __init__(self):
        Task.__init__(self, None)
        self.core = True

    def on_run(self):
        twitterpibot.hardware.on_lights_task()
