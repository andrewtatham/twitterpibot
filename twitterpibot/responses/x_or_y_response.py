import logging
import random
import re

from twitterpibot.responses.Response import Response

logger = logging.getLogger(__name__)

words = "rather|either|support|fight|win|lose"
chrs = "\?|;|:|,"
preposition = "(" + words + "|" + chrs + ")?"
pattern = preposition + "(?P<x>[\w\s]+) (or|vs) (?P<y>[\w\s]+)"
rx = re.compile(pattern, flags=re.IGNORECASE)
logger.info(pattern)


def _parse(text):
    pairs = []
    matches = rx.finditer(text)
    for match in matches:
        logger.info(match)
        x = match.group("x").strip()
        y = match.group("y").strip()

        logger.info("X = %s", x)
        logger.info("Y = %s", y)

        if _validate(x, y):
            pairs.append((x, y))
    return pairs


def _validate(x, y):
    lenx = len(x)
    leny = len(y)
    if lenx > 0 and leny > 0:
        ratio = lenx / leny
        if lenx > 3 and leny > 3 and 1 / 3 < ratio < 3:
            return True
        else:
            return False

    else:
        return False


class X_Or_Y_Response(Response):
    def condition(self, inbox_item):
        return super(X_Or_Y_Response, self).reply_condition(inbox_item) \
               and bool(rx.finditer(inbox_item.text))

    def respond(self, inbox_item):

        pairs = _parse(inbox_item.text)
        if pairs:
            for pair in pairs:
                x = pair[0]
                y = pair[1]
                # biased to Y as last is usually the comedy answer
                if random.randint(0, 2) == 0:
                    response = x
                else:
                    response = y

                self.identity.twitter.reply_with(
                    inbox_item=inbox_item,
                    text=response)
