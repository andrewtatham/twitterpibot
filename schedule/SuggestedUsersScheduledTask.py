from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from MyTwitter import MyTwitter
from colorama import Fore
from Queue import Queue
from itertools import cycle

suggestedUserColours = cycle([Fore.WHITE, Fore.CYAN])

class SuggestedUsersScheduledTask(ScheduledTask):

    def __init__(self, *args, **kwargs):
        self._slugList = Queue()       

    def GetTrigger(args):
        return IntervalTrigger(minutes=7)
    
    def onRun(args):

        with MyTwitter() as twitter:
            if args._slugList.empty():
                categories = twitter.get_user_suggestions()

                for category in categories:
                   args._slugList.put(category)

            try:
                category = args._slugList.get()
                users = twitter.get_user_suggestions_by_slug(slug = category["slug"])
                for user in users["users"]:
                    colour = suggestedUserColours.next()
                    print(colour + "U: [" + category["name"] + "] - " + user["name"] +  " [@" + user["screen_name"] + "] - " + user["description"])



            finally:
                args._slugList.task_done()


      





