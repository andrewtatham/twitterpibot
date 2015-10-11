from ScheduledTask import ScheduledTask
from Timelapse import Timelapse
import datetime 
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger


class TimelapseScheduledTask(ScheduledTask):

    #def GetTrigger(args):
    #    return IntervalTrigger(minutes = 1)


    def onRun(args):

        now = datetime.datetime.now()
        timelapse = Timelapse(
            name = 'now',
            startTime = now + datetime.timedelta(seconds = 1), 
            endTime = now + datetime.timedelta(seconds = 5),
            intervalSeconds = 1,
            tweetText = "")


        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            scheduler.add(task)



    
