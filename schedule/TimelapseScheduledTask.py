from ScheduledTask import ScheduledTask
from Timelapse import Timelapse
import datetime 
import MySchedule



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


        from MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            MySchedule.add(task)
     



    
