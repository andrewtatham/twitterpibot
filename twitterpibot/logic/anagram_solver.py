import logging

from twitterpibot.logic.dictionary import get_anagram_candidates
from twitterpibot.responses.Response import Response, unmentioned_reply_condition

screen_name = "AnagramBot"
anagram_text = "Reply to solve #Anagram"
solution_text = "The solution to the last anagram"
correct_answer_text = "got the correct answer"

logger = logging.getLogger(__name__)


def parse_anagram(text):
    return text.replace(anagram_text, "").replace(" ", "").strip().upper()


def solve_anagram(anagram):
    solutions = get_anagram_candidates(anagram)
    return solutions


class AnagramBotResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.sender and inbox_item.sender.screen_name == screen_name and \
               unmentioned_reply_condition(inbox_item, one_in=50)

    def respond(self, inbox_item):
        if anagram_text in inbox_item.text:
            anagram = parse_anagram(inbox_item.text)
            if anagram:
                logger.info("solving anagram " + anagram)
                solutions = solve_anagram(anagram)
                if solutions:
                    logger.info("solved anagram " + anagram + " found " + str(solutions))
                    for solution in solutions:
                        if solution and solution != anagram:
                            logger.info("replying to " + anagram + " with " + solution)
                            self.identity.twitter.reply_with(inbox_item=inbox_item, text=solution)
        elif correct_answer_text in inbox_item.text:
            self.identity.twitter.favourite(inbox_item.id_str)
            if self.identity.screen_name in inbox_item.text:
                self.identity.twitter.retweet(inbox_item.id_str)
        elif solution_text in inbox_item.text:
            pass


if __name__ == '__main__':
    print(solve_anagram(parse_anagram("""
    Tigers Pooch

    Reply to solve #Anagram
    """)))

if __name__ == '__main__':
    import identities
    from twitterpibot.incoming.IncomingTweet import IncomingTweet

    logging.basicConfig(level=logging.DEBUG)

    identity = identities.AndrewTathamPi2Identity(None)
    timeline = identity.twitter.get_user_timeline(screen_name=screen_name, count=1)
    tweets = list(map(lambda data: IncomingTweet(data, identity), timeline))
    tweets.reverse()
    response = AnagramBotResponse(identity)
    testcases = []

    for tweet in tweets:
        logger.info(tweet.text)
        testcases.append(tweet.text)

        if response.condition(tweet):
            logger.debug("responding to " + tweet.text)
            try:
                response.respond(tweet)
            except Exception as ex:
                logger.exception(ex)

                # pprint.pprint(testcases)
        else:
            logger.debug("Not responding to " + tweet.text)
