import logging
import random

from twitterpibot.logic import conversation
from twitterpibot.responses.Response import Response, retweet_condition, _one_in

logger = logging.getLogger(__name__)


class RetweetResponse(Response):
    def condition(self, inbox_item):
        return retweet_condition(inbox_item)

    def respond(self, inbox_item):
        logger.info("retweeting status id %s", inbox_item.id_str)
        if _one_in(10):
            self.identity.twitter.quote_tweet(inbox_item=inbox_item, text=conversation.segue())
        else:
            self.identity.twitter.retweet(inbox_item.id_str)

        if self.identity.facebook:
            self.identity.facebook.create_wall_post_from_tweet(inbox_item, "RT")


if __name__ == '__main__':
    import identities
    from twitterpibot.incoming.IncomingTweet import IncomingTweet

    logging.basicConfig(level=logging.INFO)
    identity = identities.AndrewTathamPiIdentity()
    response = RetweetResponse(identity)

    if True:
        list_name = "Awesome Bots"
        tweets = identity.twitter.get_list_statuses(
            list_id=identity.users._lists._list_ids[list_name],
            slug=list_name,
            owner_screen_name=identity.screen_name,
            owner_id=identity.id_str,
            count=200)
    else:
        tweets = identity.twitter.get_user_timeline(screen_name="andrewtathampi2")

    tweets = map(lambda tweet_data: IncomingTweet(tweet_data, identity), tweets)
    tweets = list(filter(lambda tweet: tweet.medias, tweets))
    random.shuffle(tweets)
    for i in range(1):
        tweet = tweets.pop()
        logging.info(tweet.display())
        response.respond(tweet)
