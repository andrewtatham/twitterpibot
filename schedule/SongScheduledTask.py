from ScheduledTask import ScheduledTask
from Songs import Songs
from MyTwitter import MyTwitter
import random
from OutgoingTweet import OutgoingTweet
from User import User
from apscheduler.triggers.cron import CronTrigger

class SongScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self.songs = Songs()
        
    def GetTrigger(args):
        return CronTrigger(minute = "*/5")
    def onRun(args):

        songKey = random.choice(args.songs.Keys())

        with MyTwitter() as twitter:
            target = None
            if random.randint(0,9) == 0:
                lists = twitter.show_owned_lists()
                songUsersList = filter(lambda l: l["name"] == "Song People", lists["lists"])[0]
                members = twitter.get_list_members(list_id = songUsersList["id_str"])
                target = User(random.choice(members["users"]))

            args.songs.Send(
                context = args.context, 
                songKey = songKey, 
                target = target)



