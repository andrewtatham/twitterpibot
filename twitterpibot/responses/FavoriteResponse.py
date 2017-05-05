import logging
import random

from twitterpibot.responses.Response import Response, favourite_condition

logger = logging.getLogger(__name__)


class FavoriteResponse(Response):
    def condition(self, inbox_item):
        return favourite_condition(inbox_item)

    def respond(self, inbox_item):
        logger.info("favoriting status id %s", inbox_item.id_str)
        self.identity.twitter.favourite(inbox_item.id_str)

        if self.identity.facebook:
            self.identity.facebook.create_wall_post_from_tweet(inbox_item, "Favourited")


if __name__ == '__main__':
    import identities
    from twitterpibot.incoming.IncomingTweet import IncomingTweet

    logging.basicConfig(level=logging.INFO)
    identity = identities.AndrewTathamPiIdentity()
    response = FavoriteResponse(identity)

    if True:
        list_name = "Awesome Bots"
        tweets = identity.twitter.get_list_statuses(
            list_id=identity.users.lists._list_ids[list_name],
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
