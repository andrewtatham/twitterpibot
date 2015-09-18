from Response import Response
from Timelapse import Timelapse
import datetime
class TimelapseResponse(Response):
    def Condition(args, inboxItem):
        return inboxItem.isDirectMessage and not inboxItem.from_me and inboxItem.to_me \
            and "timelapse" in inboxItem.words 

    def Respond(args, inboxItem):
        
        
        
        now = datetime.datetime.now()
        timelapse = Timelapse(
            context = args.context, 
            name = 'now',
            startTime = now + datetime.timedelta(seconds = 1), 
            endTime = now + datetime.timedelta(seconds = 5),
            intervalSeconds = 1,
            tweetText = "")


        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            args.context.scheduler.add(task)

    

    