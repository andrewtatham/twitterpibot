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
        return IntervalTrigger(minutes=17)
    
    def onRun(args):

        with MyTwitter() as twitter:
            if args._slugList.empty():
                categories = twitter.get_user_suggestions()

                for category in categories:
                    colour = suggestedUserColours.next()
                    print(colour + "Users: [" + category["name"] + "]")
                    args._slugList.put(category)

            try:
                category = args._slugList.get()
                suggestedUsers = twitter.get_user_suggestions_by_slug(slug = category["slug"])
                for user in suggestedUsers["users"]:
                    colour = suggestedUserColours.next()
                    print(colour + "User: [" + category["name"] + "] - " + user["name"] +  " [@" + user["screen_name"] + "] - " + user["description"].replace("\n", "   "))



            finally:
                args._slugList.task_done()


      





