from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.twitter.MyTwitter import MyTwitter
from colorama import Fore
from itertools import cycle

suggestedUserColours = cycle([Fore.WHITE, Fore.CYAN])


class SuggestedUsersScheduledTask(ScheduledTask):
    def __init__(self):
        self._slugList = []

    def GetTrigger(self):
        return IntervalTrigger(minutes=17)

    def onRun(self):

        with MyTwitter() as twitter:
            if not self._slugList:
                categories = twitter.get_user_suggestions()

                for category in categories:
                    colour = next(suggestedUserColours)
                    print(colour + "Users: [" + category["name"] + "]")
                    self._slugList.append(category)

            category = self._slugList.pop()
            suggestedUsers = twitter.get_user_suggestions_by_slug(slug=category["slug"])
            for user in suggestedUsers["users"]:
                colour = next(suggestedUserColours)
                print(colour + "User: [" + category["name"] + "] - " + user["name"] + " [@" + user["screen_name"] + "] - " + user["description"].replace("\n", "   "))
