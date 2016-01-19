from unittest import TestCase
from twitterpibot.schedule.RegularTimelapseScheduledTask import RegularTimelapseScheduledTask

__author__ = 'andrewtatham'


class TestRegularTimelapseScheduledTask(TestCase):
    def test_onRun(self):
        task = RegularTimelapseScheduledTask()
        task.onRun()
