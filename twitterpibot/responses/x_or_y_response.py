import logging
import random
import re

from twitterpibot.logic import magic8ball

from twitterpibot.responses.Response import Response

logger = logging.getLogger(__name__)

words = "rather|either|support|fight|win|lose"
chrs = "\?|;|:|,"
preposition = ".*(" + words + "|" + chrs + ")?"
pattern = preposition + "(?P<x>[\w\s]+) (or|vs) (?P<y>[\w\s]+) ?\?"
rx = re.compile(pattern, flags=re.IGNORECASE)
logger.info(pattern)


def _parse(text):
    pairs = []
    matches = rx.finditer(text)
    for match in matches:
        logger.info(match)
        x = match.group("x").strip()
        y = match.group("y").strip()
        if _validate(x, y):
            pairs.append((x, y))
    return pairs


def _validate(x, y):
    logger.info("X = %s", x)
    logger.info("Y = %s", y)
    lenx = len(x)
    leny = len(y)
    if lenx > 0 and leny > 0:
        ratio = lenx / leny
        logger.info("ratio = %s", ratio)
        if lenx > 3 and leny > 3 and 1 / 7 < ratio < 7:
            logger.info("valid")
            return True
    logger.info("invalid")
    return False


class X_Or_Y_Response(Response):
    def condition(self, inbox_item):
        return (super(X_Or_Y_Response, self).mentioned_reply_condition(inbox_item)
                or super(X_Or_Y_Response, self).unmentioned_reply_condition(inbox_item)) \
               and bool(_parse(inbox_item.text_stripped))

    def respond(self, inbox_item):
        pairs = _parse(inbox_item.text_stripped)
        if pairs:
            for pair in pairs:
                x = pair[0]
                y = pair[1]
                # biased to Y as last is usually the comedy answer
                if random.randint(0, 2) == 0:
                    response = x
                else:
                    response = y
                file_paths = None
                if inbox_item.is_tweet:
                    file_paths = [magic8ball.get_image(response)]
                    response += " #Magic8Ball"
                self.identity.twitter.reply_with(
                    inbox_item=inbox_item,
                    text=response,
                    file_paths=file_paths)
