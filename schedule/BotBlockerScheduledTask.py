from ScheduledTask import ScheduledTask
from BotBlocker import BotBlocker
from MyTwitter import MyTwitter
from apscheduler.triggers.interval import IntervalTrigger
class BotBlockerScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self.blocker = BotBlocker()
        self.page = "-1"
        self.myFollowers = []     


    #def GetTrigger(args):
    #    return IntervalTrigger(minutes=3)

    def onRun(args):
        blockUsers = []
        with MyTwitter() as twitter:
            if not any(args.myFollowers):


                #response = twitter.get_followers_list(cursor = args.page)
                #args.myFollowers.extend(response["users"])

                response = twitter.get_followers_ids(cursor = args.page,stringify_ids=True)
                args.myFollowers.extend(response["ids"])

                nextPage = response["next_cursor_str"]
                if nextPage == "0":
                    args.page = "-1"
                else:
                    args.page = nextPage

            if any(args.myFollowers):
                follower = args.myFollowers.pop()

                user = args.context.users.getUser(id = follower)

                block = args.blocker.IsUserBot(user)
                if block:
                     args.blocker.BlockUser(user)

        
    