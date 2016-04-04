import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.logic import jokes


class JokesScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(2, 5), minutes=random.randint(0, 59))

    def on_run(self):
        text = jokes.get_joke()
        if text:
            self.identity.twitter.send(OutgoingTweet(text=text))


if __name__ == '__main__':
    import main

    identity = main.AndrewTathamPiIdentity(None)
    task = JokesScheduledTask(identity)
    task.on_run()
