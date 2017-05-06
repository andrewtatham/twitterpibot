import logging
import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class ResponsesScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(ResponsesScheduledTask, self).__init__(identity)
        self._responses = self.identity.get_responses()

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        list_id = self.identity.users.lists.get_list_id("Need Input")
        tweets_data = self.identity.twitter.get_list_statuses(list_id=list_id)
        tweets = list(map(lambda data: IncomingTweet(data, self.identity), tweets_data))
        for tweet in tweets:
            logging.info(tweet.display())
            for response in self._responses:
                if response.condition(tweet):
                    response.respond(tweet)


if __name__ == '__main__':
    import identities
    logging.basicConfig(level=logging.INFO)

    andrewtatham = identities.AndrewTathamIdentity()
    andrewtathampi = identities.AndrewTathamPiIdentity(andrewtatham)
    andrewtathampi2 = identities.AndrewTathamPi2Identity(andrewtatham)

    andrewtathampi.converse_with = andrewtathampi2
    andrewtathampi2.converse_with = andrewtathampi

    task = ResponsesScheduledTask(andrewtathampi)
    task.on_run()
