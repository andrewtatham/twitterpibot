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
        return IntervalTrigger(hours=11, minutes=3)

    def on_run(self):
        birthday_users = Birthdays.get_birthday_users()
        if birthday_users:
            for birthday_user in birthday_users:
                birthday_song_key = random.choice(self.songs.birthday_song_keys())
                birthday_song = self.songs.get_song(song_key=birthday_song_key)
                self.identity.twitter.sing_song(
                    song=birthday_song,
                    target=birthday_user,
                    text="Happy Birthday @" + birthday_user + " !!!",
                    hashtag="#HappyBirthday")

        else:
            song_key = random.choice(self.songs.keys())
            song = self.songs.get_song(song_key=song_key)
            if song:
                self.identity.twitter.sing_song(song=song)
