import logging
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.twitter.MyTwitter import MyTwitter
from colorama import Fore
from itertools import cycle
# import random

suggestedUserColours = cycle([Fore.WHITE, Fore.CYAN])


class SuggestedUsersScheduledTask(ScheduledTask):
    def __init__(self):
        super(SuggestedUsersScheduledTask, self).__init__()
        self._slugList = []

    def GetTrigger(self):
        return IntervalTrigger(minutes=17)

    def onRun(self):

        with MyTwitter() as twitter:
            if not self._slugList:
                categories = twitter.get_user_suggestions()

                for category in categories:
                    colour = next(suggestedUserColours)
                    logging.info(colour + "Users: [" + category["name"] + "]")
                    self._slugList.append(category)

            category = self._slugList.pop()
            suggested_users = twitter.get_user_suggestions_by_slug(slug=category["slug"])["users"]
            for user in suggested_users:
                colour = next(suggestedUserColours)
                logging.info(colour + "User: [" + category["name"] + "] - " + user["name"] + " [@" + user[
                    "screen_name"] + "] - " + user["description"].replace("\n", "   "))

            # if random.randint(0, 2) == 0:
            #     user = random.choice(suggested_users)
            #     logging.info("[SuggestedUsersScheduledTask] following " + user["name"] + " [@" + user["screen_name"] + "]")
            #     twitter.create_friendship(id=user["id_str"])
