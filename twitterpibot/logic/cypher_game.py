import json
import logging

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic import judgement_day, cypher_breaker
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.responses.Response import Response
from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)

_cypher = cypher_breaker.RandomCypher()
_breaker = cypher_breaker.RandomCypherBreaker()


def next_game(twitter=None):
    _cypher.reset()
    _breaker.reset()
    personality = judgement_day.next_personality()
    _update_profile(twitter, personality)


def _update_profile(twitter, personality):
    if twitter and personality:
        twitter.update_profile(profile_link_color=personality.colour)
        twitter.update_profile_image(file_path=personality.profile_image)
        twitter.update_profile_banner_image(file_path=personality.banner_image)


class CypherHostMidnightScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(CypherHostMidnightScheduledTask, self).__init__(identity)

    def get_trigger(self):
        return CronTrigger(hour="0")

    def on_run(self):
        next_game(self.identity.twitter)


class CypherHostScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(CypherHostScheduledTask, self).__init__(identity)

    def get_trigger(self):
        return CronTrigger(hour="*")
        # return CronTrigger(minute="*/5")

    def on_run(self):
        text = judgement_day.phrase()
        code = _cypher.encode(text)
        tweet_id = self.identity.twitter.send(OutgoingTweet(text=code))
        self.identity.conversations.track_replies(tweet_id, self.on_response)

    def on_response(self, inbox_item):
        logger.info("RESPONSE RECIEVED")
        inbox_item.display()


class CypherHostResponse(Response):
    def condition(self, inbox_item):
        if inbox_item.is_tweet or inbox_item.is_direct_message:
            guess = cypher_breaker.is_guess(inbox_item.text_stripped)
            if guess:
                score = _cypher.score_guess(guess)
                return inbox_item.is_direct_message \
                       and guess \
                       and score > 0.8

    def respond(self, inbox_item):
        next_game(self.identity.twitter)


class DecypherScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(DecypherScheduledTask, self).__init__(identity)

    def get_trigger(self):
        return CronTrigger(hour="*/2")

    def on_run(self):
        for _ in range(2):
            # todo remove this blatant cheat
            _breaker.add_expected_phrase(judgement_day.phrase())


class DecypherResponse(Response):
    def __init__(self, identity):
        super(DecypherResponse, self).__init__(identity)

    def condition(self, inbox_item):
        return inbox_item.is_tweet \
               and inbox_item.sender.screen_name == "THEMACHINESCODE" \
               and cypher_breaker.is_cypher(inbox_item.text_stripped)

    def respond(self, inbox_item):

        _breaker.add_code(inbox_item.text_stripped)

        guess = _breaker.get_guess()

        logger.info(guess)

        if guess.estimated_score > 0.5:
            guess_cypher = cypher_breaker.SubstitutionCypher(guess.encode, guess.decode)
            decoded_text = guess_cypher.decode(inbox_item.text_stripped)
            logger.info("Decoded: " + decoded_text)
            self.identity.twitter.quote_tweet(inbox_item=inbox_item, text=decoded_text)
            if guess.estimated_score > 0.8:
                guess_string = json.dumps(guess)
                inbox_item.twitter.reply_with(inbox_item=inbox_item, text=guess_string, as_direct_message=True)

# if __name__ == '__main__':
#     import identities
#
#     identity = identities.TheMachinesCodeIdentity()
#     task = CypherHostMidnightScheduledTask(identity)
#     # task = CypherHostScheduledTask(identity)
#     task.on_run()
#
# if __name__ == '__main__':
#     from twitterpibot.incoming.IncomingTweet import IncomingTweet
#     import identities
#
#     tweet_id = "723749492051304449"
#     identity = identities.AndrewTathamPi2Identity()
#     tweet_data = identity.twitter.twitter.lookup_status(id=[tweet_id])[0]
#     pprint.pprint(tweet_data)
#     tweet = IncomingTweet(tweet_data, identity)
#
#     response = DecypherResponse(identity)
#     print(response.condition(tweet))
#     response.respond(tweet)
