import logging
from twitterpibot.Identity import get_responses

logger = logging.getLogger(__name__)


class ResponseFactory(object):
    def __init__(self):
        self.responses = get_responses()
        for response in self.responses:
            logger.info("[ResponseFactory] adding " + str(type(response)))

    def create(self, inbox_item):
        if inbox_item:
            for response in self.responses:
                if response.condition(inbox_item):
                    response.respond(inbox_item)
                    break
        return None
