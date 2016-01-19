import random
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.processing import Birthdays
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.songs.Songs import Songs


class SongScheduledTask(ScheduledTask):
    def __init__(self):
        super(SongScheduledTask, self).__init__()
        self.songs = Songs()

    def GetTrigger(self):
        return IntervalTrigger(hours=32)

    def onRun(self):

        birthday_users = Birthdays.get_birthday_users()
        if birthday_users:
            for birthdayUser in birthday_users:
                Birthdays.sing_birthday_song(birthdayUser)
        else:
            song_key = random.choice(self.songs.Keys())
            self.songs.Send(song_key=song_key)
