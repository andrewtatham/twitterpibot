import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.songs import songhelper


class SongScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(SongScheduledTask, self).__init__(identity)

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(72, 96), minutes=random.randint(0, 59))

    def on_run(self):
        song_key = random.choice(songhelper.keys())
        song = songhelper.get_song(song_key=song_key)
        if song:
            self.identity.twitter.sing_song(song=song)

if __name__ == '__main__':
    import identities_pis
    identity = identities_pis.AndrewTathamPiIdentity()
    task = SongScheduledTask(identity)
    task.on_run()