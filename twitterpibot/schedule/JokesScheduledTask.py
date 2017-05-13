import random

from apscheduler.triggers.interval import IntervalTrigger

import identities_pis
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.logic import jokes


class JokesScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(24, 48), minutes=random.randint(0, 59))

    def on_run(self):
        text = jokes.get_joke()
        if text:
            self.identity.twitter.send(OutgoingTweet(text=text))

            if self.identity.facebook:
                self.identity.facebook.create_wall_post(text)


if __name__ == '__main__':
    identity = identities_pis.AndrewTathamPiIdentity(None)
    task = JokesScheduledTask(identity)
    task.on_run()
