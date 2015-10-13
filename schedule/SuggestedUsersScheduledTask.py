from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from MyTwitter import MyTwitter
from colorama import Fore
from itertools import cycle

suggestedUserColours = cycle([Fore.WHITE, Fore.CYAN])

class SuggestedUsersScheduledTask(ScheduledTask):

    def __init__(self, *args, **kwargs):
        self._slugList = [] 

    def GetTrigger(args):
        return IntervalTrigger(minutes=17)
    
    def onRun(args):

        with MyTwitter() as twitter:
            if not args._slugList:
                categories = twitter.get_user_suggestions()

                for category in categories:
                    colour = next(suggestedUserColours)
                    print(colour + "Users: [" + category["name"] + "]")
                    args._slugList.append(category)
 
            category = args._slugList.pop()
            suggestedUsers = twitter.get_user_suggestions_by_slug(slug = category["slug"])
            for user in suggestedUsers["users"]:
                colour = next(suggestedUserColours)
                print(colour + "User: [" + category["name"] + "] - " + user["name"] +  " [@" + user["screen_name"] + "] - " + user["description"].replace("\n", "   "))



      





