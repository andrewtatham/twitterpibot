from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage
from twitterpibot.incoming.IncomingEvent import IncomingEvent
import logging

logger = logging.getLogger(__name__)


def Create(data):
    if "text" in data:
        return IncomingTweet(data)
    elif "direct_message" in data:
        return IncomingDirectMessage(data)
    elif "event" in data:
        return IncomingEvent(data)
    elif "friends" in data:
        logger.info("Connected...")
    else:
        logger.debug(data)


