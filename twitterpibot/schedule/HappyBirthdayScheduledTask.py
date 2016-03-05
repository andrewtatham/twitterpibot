import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
import twitterpibot.processing.Birthdays as Birthdays
from twitterpibot.songs.Songs import Songs


class HappyBirthdayScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour="8-20/2")

    def on_run(self):
        songs = Songs()
        birthday_users = Birthdays.get_birthday_users()
        if birthday_users:
            for birthday_user in birthday_users:
                birthday_song_key = random.choice(songs.birthday_song_keys())
                birthday_song = songs.get_song(song_key=birthday_song_key)
                self.identity.twitter.sing_song(
                    song=birthday_song,
                    target=birthday_user,
                    text="Happy Birthday @" + birthday_user + " !!!",
                    hashtag="#HappyBirthday")
