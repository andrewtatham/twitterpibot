from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.songs.Songs import Songs
from twitterpibot.twitter.MyTwitter import MyTwitter
import random

from apscheduler.triggers.cron import CronTrigger
from twitterpibot.users import Users


class SongScheduledTask(ScheduledTask):
    def __init__(self):
        super(SongScheduledTask, self).__init__()
        self.songs = Songs()

    def GetTrigger(self):
        return CronTrigger(hour="8-22/3")

    def onRun(self):
        song_key = random.choice(self.songs.Keys())

        with MyTwitter() as twitter:
            target = None
            if random.randint(0, 9) == 0:
                lists = twitter.show_owned_lists()
                song_users_list = filter(lambda l: l["name"] == "Song People", lists["lists"])
                list_id = song_users_list["id_str"]
                members = twitter.get_list_members(list_id=int(list_id))
                target = Users.get_user(user_data=random.choice(members["users"]))

            self.songs.Send(
                song_key=song_key,
                target=target)
