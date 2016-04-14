from unittest import TestCase

from twitterpibot.schedule.timelapse.RegularTimelapseScheduledTask import RegularTimelapseScheduledTask


class TestRegularTimelapseScheduledTask(TestCase):
    def test_onRun(self):
        task = RegularTimelapseScheduledTask(None)
        task.on_run()
