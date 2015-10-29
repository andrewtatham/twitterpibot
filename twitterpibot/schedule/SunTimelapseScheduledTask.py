from apscheduler.triggers.cron import CronTrigger
from processing.MyAstral import GetTimes

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.processing.Timelapse import Timelapse


class SunTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=3)

    def onRun(self):
        sun = GetTimes()

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
