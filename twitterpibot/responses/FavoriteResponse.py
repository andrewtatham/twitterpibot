import logging

from twitterpibot.responses.Response import Response, favourite_condition

logger = logging.getLogger(__name__)


class FavoriteResponse(Response):
    def condition(self, inbox_item):
        return favourite_condition(inbox_item)

    def respond(self, inbox_item):
        logger.info("favoriting status id %s", inbox_item.id_str)
        self.identity.twitter.create_favorite(inbox_item.id_str)
