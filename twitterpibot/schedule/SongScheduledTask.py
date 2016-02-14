import random
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.processing import Birthdays
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.songs.Songs import Songs


class SongScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(SongScheduledTask, self).__init__(identity)
        self.songs = Songs()

    def get_trigger(self):
        return IntervalTrigger(hours=32)

    def on_run(self):

        birthday_users = Birthdays.get_birthday_users()
        if birthday_users:
            for birthdayUser in birthday_users:
                Birthdays.sing_birthday_song(self.identity, screen_name=birthdayUser)
        else:
            song_key = random.choice(self.songs.keys())
            self.songs.sing_song(self.identity, song_key=song_key)
