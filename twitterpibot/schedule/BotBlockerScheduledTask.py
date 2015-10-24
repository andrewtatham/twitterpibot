from twitterpibot.schedule.ScheduledTask import ScheduledTask

from twitterpibot.users.BotBlocker import BotBlocker
from twitterpibot.twitter.MyTwitter import MyTwitter
from apscheduler.triggers.interval import IntervalTrigger
import twitterpibot.users.Users as Users


class BotBlockerScheduledTask(ScheduledTask):
    def __init__(self):
        super(BotBlockerScheduledTask, self).__init__()
        self._blocker = BotBlocker()
        self._page = "-1"
        self._myFollowers = []

    def GetTrigger(self):
        return IntervalTrigger(minutes=13)

    def onRun(self):
        with MyTwitter() as twitter:
            if not any(self._myFollowers):

                # response = twitter.get_followers_list(cursor = args.page)
                # args.myFollowers.extend(response["users"])

                response = twitter.get_followers_ids(cursor=self._page, stringify_ids=True)
                self._myFollowers.extend(response["ids"])

                nextPage = response["next_cursor_str"]
                if nextPage == "0":
                    self._page = "-1"
                else:
                    self._page = nextPage

            if any(self._myFollowers):
                followerId = self._myFollowers.pop()

                usr = Users.getUser(id=followerId)

                block = self._blocker.IsUserBot(usr)
                if block:
                    self._blocker.BlockUser(usr)
