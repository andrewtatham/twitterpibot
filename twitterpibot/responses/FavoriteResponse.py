import logging

from twitterpibot.responses.Response import Response

logger = logging.getLogger(__name__)


class FavoriteResponse(Response):
    def condition(self, inbox_item):
        return favourite_condition(inbox_item)

    def respond(self, inbox_item):
        logger.info("favoriting status id %s", inbox_item.status_id)
        self.identity.twitter.create_favorite(inbox_item.status_id)
