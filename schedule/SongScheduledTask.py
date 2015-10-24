from ScheduledTask import ScheduledTask
from Songs import Songs
from MyTwitter import MyTwitter
import random
import Users

from apscheduler.triggers.cron import CronTrigger

class SongScheduledTask(ScheduledTask):
    def __init__(self):
        self.songs = Songs()
        
    def GetTrigger(self):
        return CronTrigger(hour = "8-22/3")
    def onRun(self):

        songKey = random.choice(self.songs.Keys())

        with MyTwitter() as twitter:
            target = None
            if random.randint(0,9) == 0:
                lists = twitter.show_owned_lists()
                songUsersList = filter(lambda l: l["name"] == "Song People", lists["lists"])[0]
                listId = songUsersList["id_str"]
                members = twitter.get_list_members(list_id = listId)
                target = Users.getUser(data = random.choice(members["users"]))

            self.songs.Send(
                songKey = songKey, 
                target = target)



