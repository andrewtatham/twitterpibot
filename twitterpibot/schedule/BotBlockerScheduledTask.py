import logging
import os
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.schedule.ScheduledTask import ScheduledTask
import twitterpibot.users.BotBlocker as BotBlocker
from twitterpibot.twitter.MyTwitter import MyTwitter
import twitterpibot.users.Users as Users


class BotBlockerScheduledTask(ScheduledTask):
    def __init__(self):
        super(BotBlockerScheduledTask, self).__init__()
        self._page = "-1"
        self._myFollowers = []

    def GetTrigger(self):
        return IntervalTrigger(minutes=6)

    def onRun(self):
        with MyTwitter() as twitter:
            if not any(self._myFollowers):
                response = twitter.get_followers_ids(cursor=self._page, stringify_ids=True)
                self._myFollowers.extend(response["ids"])
                next_page = response["next_cursor_str"]
                if next_page == "0":
                    self._page = "-1"
                else:
                    self._page = next_page

            if any(self._myFollowers):
                follower_id = self._myFollowers.pop()
                usr = Users.get_user(user_id=follower_id)
                BotBlocker.check_user(usr)

if __name__ == "__main__":
    os.chdir("../../")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    task = BotBlockerScheduledTask()
    for i in range(5):
        task.onRun()
