from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
import twitterpibot.processing.MyAstral as MyAstral
from twitterpibot.processing.Timelapse import Timelapse


class NightTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=15)

    def onRun(self):
        today = MyAstral.GetTimes()
        tommorrow = MyAstral.GetTommorrowTimes()

        timelapse = Timelapse(
            name='night',
            startTime=today['sunset'],
            endTime=tommorrow['sunrise'],
            intervalSeconds=600,
            tweetText="The cosmic ballet goes on...")

        from twitterpibot.schedule.MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)
