from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.processing.MyAstral import MyAstral
from twitterpibot.processing.Timelapse import Timelapse


class SunTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=3, minute=1)

    def onRun(self):
        sun = MyAstral().GetTimes()

        timelapse = Timelapse(
            name='sun',
            startTime=sun['dawn'],
            endTime=sun['dusk'],
            intervalSeconds=600,
            tweetText="The cosmic ballet goes on...")

        from twitterpibot.schedule.MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)
