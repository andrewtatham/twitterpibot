import random
import re
import logging

from twitterpibot.responses.Response import Response
from twitterpibot.twitter import TwitterHelper

logger = logging.getLogger(__name__)


class FavoriteResponse(Response):
    def __init__(self):
        self.bannedTopics = [

            # TODO move to topics

            # RT to Win
            "(RT|Retweet|chance|follow).*(to|2).*win",

            # RT/Fav voting
            "(RT|Retweet).*(Fav)",
            "(Fav).*(RT|Retweet)",

        ]

        self.rx = re.compile("|".join(self.bannedTopics), re.IGNORECASE)

    def condition(self, inbox_item):
        return inbox_item.is_tweet \
               and not inbox_item.from_me \
               and not inbox_item.to_me \
               and not (inbox_item.favorited or inbox_item.retweeted_status and inbox_item.retweeted_status.favorited) \
               and not inbox_item.sender.is_arsehole \
               and not bool(self.rx.match(inbox_item.text)) \
               and (not inbox_item.topics or inbox_item.topics.retweet()) \
               and ((inbox_item.sender.is_bot and random.randint(0, 50) == 0) or
                    (inbox_item.sender.is_friend and random.randint(0, 3) == 0) or
                    (inbox_item.sourceIsTrend and random.randint(0, 20) == 0) or
                    (inbox_item.sourceIsSearch and random.randint(0, 20) == 0) or
                    (random.randint(0, 99) == 0))

    def respond(self, inbox_item):
        logger.info("favoriting status id %s", inbox_item.status_id)
        TwitterHelper.create_favorite(inbox_item.status_id)