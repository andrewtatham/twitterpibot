from ScheduledTask import ScheduledTask
from BotBlocker import BotBlocker
from MyTwitter import MyTwitter
class BotBlockerScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self.blocker = BotBlocker()
        self.page = "-1"
        self.myFollowers = []     


    def GetTrigger(args):
        return super(BotBlockerScheduledTask, args).GetTrigger()

    def onInit(args):
        return super(BotBlockerScheduledTask, args).onInit()

    def onRun(args):
        blockUsers = []
        with MyTwitter() as twitter:
            if not any(args.myFollowers):
                response = twitter.get_followers_list(cursor = args.page)
                args.myFollowers.extend(response["users"])
                nextPage = response["next_cursor_str"]
                if nextPage == "0":
                    args.page = "-1"
                else:
                    args.page = nextPage

            if any(args.myFollowers):
                follower = args.myFollowers.pop()
                block = args.blocker.IsUserBot(user_id = follower["id_str"], username = follower["name"], screen_name = follower["screen_name"], description = follower["description"])
                if block:
                    twitter.create_block(user_id = follower["id_str"], screen_name = follower["screen_name"])

        
    