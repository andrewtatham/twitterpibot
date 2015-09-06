from ScheduledTask import ScheduledTask
from MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from Timelapse import Timelapse
class SunsetTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour=15,minute=0)


    def onRun(args):

        sun = MyAstral().GetTimes()

        timelapse = Timelapse(
            context = args.context, 
            name = 'sunset',
            startTime = sun['sunset'], 
            endTime = sun['dusk'],
            intervalSeconds = 90,
            tweetText = "Goodnight!")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            args.context.scheduler.add(task)

