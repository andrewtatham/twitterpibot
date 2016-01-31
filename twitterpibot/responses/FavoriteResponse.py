import logging

from twitterpibot.responses.Response import Response
from twitterpibot.twitter import TwitterHelper

logger = logging.getLogger(__name__)


class FavoriteResponse(Response):
    def condition(self, inbox_item):
        return super(FavoriteResponse, self).favourite_condition(inbox_item)

    def respond(self, inbox_item):
        logger.info("favoriting status id %s", inbox_item.status_id)
        TwitterHelper.create_favorite(inbox_item.status_id)
