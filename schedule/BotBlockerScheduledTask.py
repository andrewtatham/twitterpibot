from ScheduledTask import ScheduledTask
from BotBlocker import BotBlocker
from MyTwitter import MyTwitter
from apscheduler.triggers.interval import IntervalTrigger
import Users



class BotBlockerScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self._blocker = BotBlocker()
        self._page = "-1"
        self._myFollowers = []     


    def GetTrigger(args):
        return IntervalTrigger(minutes=13)

    def onRun(args):
        blockUsers = []
        with MyTwitter() as twitter:
            if not any(args._myFollowers):


                #response = twitter.get_followers_list(cursor = args.page)
                #args.myFollowers.extend(response["users"])

                response = twitter.get_followers_ids(cursor = args._page,stringify_ids=True)
                args._myFollowers.extend(response["ids"])

                nextPage = response["next_cursor_str"]
                if nextPage == "0":
                    args._page = "-1"
                else:
                    args._page = nextPage

            if any(args._myFollowers):
                follower = args._myFollowers.pop()

                user = Users.getUser(id = follower)

                block = args._blocker.IsUserBot(user)
                if block:
                     args._blocker.BlockUser(user)

        
    