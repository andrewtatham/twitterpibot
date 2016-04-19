from collections import Counter
import logging
import pprint
from twitterpibot.incoming.IncomingTweet import IncomingTweet

from twitterpibot.logic.cypher_helper import _map
from twitterpibot.responses.Response import Response, mentioned_reply_condition, unmentioned_reply_condition

logger = logging.getLogger(__name__)

_encode = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    " ": "  ",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----"
}

_decode = dict([(v, k) for k, v in _encode.items()])


def is_morse_code(text):
    count = Counter(text)
    dots = count["."]
    dash = count["-"]
    space = count[" "]
    factor = (dots + dash + space) / len(text)
    return factor >= 0.75


def encode(text):
    code = " ".join(map(lambda letter: _map(_encode, letter), text))
    return code


def decode(code):
    text = " ".join(map(_decode_word, code.split("  ")))
    return text


def _decode_word(word):
    return "".join(map(lambda letter: _map(_decode, letter), list(word.strip().split(" "))))


class MorseCodeResponse(Response):
    def condition(self, inbox_item):
        return (
                   mentioned_reply_condition(inbox_item) or
                   unmentioned_reply_condition(inbox_item)
               ) and is_morse_code(inbox_item.text)

    def respond(self, inbox_item):
        code = decode(inbox_item.text)
        self.identity.twitter.quote_tweet(inbox_item, code)


# TODO MORSE CODE

# TODO OTHER CYPHERS
# TODO BREAK CYPHER
if __name__ == '__main__':
    # code = "_@andrewtathampi2 --... .... ....- --... .---- ..... --... .... ...-- ..... " \
    #        '----- ..- -. -.. ----- ..-. .---- -. ...-- ...- .---- --...' \
    #        '....- ---.. .---- .-.. .---- --... -.--'
    # print(is_morse_code(code))
    # text = decode(code)
    # print(text)

    import identities

    logging.basicConfig(level=logging.DEBUG)

    identity = identities.AndrewTathamPi2Identity(None)
    timeline = identity.twitter.get_user_timeline(screen_name="andrewtathampi", count=10)
    tweets = list(map(lambda data: IncomingTweet(data, identity), timeline))
    tweets.reverse()
    response = MorseCodeResponse(identity)

    for tweet in tweets:
        logger.info(tweet.display())

        if response.condition(tweet):
            try:
                response.respond(tweet)
            except Exception as ex:
                logger.exception(ex)
