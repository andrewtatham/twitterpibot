import logging
import random
import re

from twitterpibot.logic import magic8ball
from twitterpibot.responses.Response import Response

logger = logging.getLogger(__name__)

words = "rather"
chrs = "\?|;|:|,|\."
preposition = "(?P<pre>.*(" + words + "|" + chrs + "))? ?"
post = " ?(?P<post>("+chrs+").*)"
pattern = preposition + "(?P<x>[#\w\s]+) (or|vs) (?P<y>[#\w\s]+)" + post
rx = re.compile(pattern, flags=re.IGNORECASE)
logger.debug(pattern)


def _parse(text):
    result = []
    matches = rx.finditer(text)
    for match in matches:
        logger.info(match)
        x = match.group("x").strip()
        y = match.group("y").strip()
        pre = match.group("pre")
        post = match.group("post")
        if pre:
            pre=pre.strip()
        if post:
            post=post.strip()
        if _validate(x, y):
            result.append({"pre": pre, "x": x, "y": y, "post": post})
    return result


def _validate(x, y):
    logger.info("X = %s", x)
    logger.info("Y = %s", y)
    lenx = len(x)
    leny = len(y)
    logger.info("lenx = %s", lenx)
    logger.info("leny = %s", leny)

    if lenx > 3 and leny > 3:
        ratio = lenx / leny
        logger.info("ratio = %s", ratio)
        if (1 / 7) < ratio < 7:
            logger.info("valid >3")
            return True
        else:
            logger.info("invalid >3")
            return False
    elif lenx > 0 and leny > 0:
        logger.info("valid >1")
        return True
    else:
        logger.info("invalid <1")
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
                x = pair["x"]
                y = pair["y"]
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
