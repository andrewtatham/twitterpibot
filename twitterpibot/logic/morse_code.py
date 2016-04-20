from collections import Counter
import logging
import pprint
from twitterpibot.incoming.IncomingTweet import IncomingTweet

from twitterpibot.logic.cypher_helper import _map, SubstitutionCypher
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


class MorseCode(SubstitutionCypher):
    def __init__(self):
        super(MorseCode, self).__init__(_encode, _decode,
                                        encode_out_sep=" ", encode_out_word_sep="  ",
                                        decode_in_word_sep="  ", decode_in_sep=" ")


class MorseCodeResponse(Response):
    morse = MorseCode()

    def condition(self, inbox_item):
        return (
                   mentioned_reply_condition(inbox_item) or
                   unmentioned_reply_condition(inbox_item)
               ) and is_morse_code(inbox_item.text)

    def respond(self, inbox_item):
        decoded = self.morse.decode(inbox_item.text)
        self.identity.twitter.quote_tweet(inbox_item, decoded)


if __name__ == '__main__':


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
