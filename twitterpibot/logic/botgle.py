import logging
import pprint
import random

from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.logic import botgle_solver, botgle_artist
from twitterpibot.outgoing import OutgoingDirectMessage
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.responses.Response import Response

logger = logging.getLogger(__name__)
descriptions = [
    "this piece is titled: %s",
    "piece titled: %s",
    "title: %s",
]


class BotgleGame(object):
    def __init__(self, identity):
        self.board_in_progress = None
        self.solution = None
        self.identity = identity

    def read_tweet(self, inbox_item):
        retval = {}
        board = botgle_solver.parse_board(inbox_item.text)
        if board:
            retval["board"] = board
            if not self.board_in_progress or self.board_in_progress != board:
                # start new solver
                self.solution = None
                self.board_in_progress = board

                self.solution = botgle_solver.solve_board(self.board_in_progress)

                if self.solution:
                    retval["solutions"] = self.solution
            if self.board_in_progress and self.board_in_progress == board:
                # solution in progress
                # retval["text"] = "[painting noises]"
                pass

        elif "GAME OVER" in inbox_item.text:
            if self.board_in_progress and self.solution:
                image = botgle_artist.make(self.board_in_progress, self.solution, self.identity.screen_name)
                retval["image"] = image
            self.board_in_progress = None
            self.solution = None
        elif "Boggle in 10 minutes" in inbox_item.text:
            retval["text"] = random.choice([
                "[mixes paint]",
                "[fetches easel]",
                "[gets canvas]",
                "[prepares canvas]",
            ])
        elif "Next game in 6 hours" in inbox_item.text:
            retval["text"] = random.choice([
                "[buys paint]",
                "[buys canvas]",
                "[buys brushes]",
                "[cleans brushes]",
                "[sleeps]"
            ])
        return retval


class BotgleResponse(Response):
    def __init__(self, identity, armed=True):
        super(BotgleResponse, self).__init__(identity)
        self._game = BotgleGame(identity)
        self._armed = armed

    def condition(self, inbox_item):
        return inbox_item.is_tweet and inbox_item.sender.screen_name == "Botgle"

    def respond(self, inbox_item):
        response = self._game.read_tweet(inbox_item)
        if response:
            logger.debug(pprint.pformat(response))
            if "image" in response:
                image = response["image"]
                if image and "name" in image and "file_path" in image:
                    text = ""
                    text += random.choice(descriptions) % image["name"]
                    file_paths = [image["file_path"]]
                    if self._armed:
                        self.identity.twitter.send(OutgoingTweet(text=text, file_paths=file_paths))
                    else:
                        logger.info("tweets " + text + " " + str(file_paths))
                    if random.randint(0, 9) == 0:
                        file_path = image["file_path"]
                        if self._armed:
                            self.identity.twitter.update_profile_image(file_path=file_path)
                        else:
                            logger.info("updates profile image " + file_path)
            elif "solutions" in response:
                if "text" in response:
                    text = response["text"]
                    if self._armed:
                        self.identity.twitter.send(OutgoingTweet(text=text))
                    else:
                        logger.info(text)
                solutions = response["solutions"]
                if solutions:
                    words = list(solutions)
                    words.sort(key=len)
                    words = words[-10:]
                    words.reverse()
                    text = ""
                    text += ("%s words found " % len(solutions))
                    text += " ".join(words)
                    if self._armed:
                        self.identity.twitter.send(
                            OutgoingDirectMessage.OutgoingDirectMessage(text=text, screen_name="andrewtatham"))
                    else:
                        logger.info(text)

            elif "text" in response:
                text = response["text"]
                if self._armed:
                    self.identity.twitter.send(OutgoingTweet(text=text))
                else:
                    logger.info(text)


if __name__ == '__main__':
    import main

    logging.basicConfig(level=logging.INFO)

    identity = main.BotgleArtistIdentity(None)
    timeline = identity.twitter.get_user_timeline(screen_name="botgle", exclude_replies=True, count=200)
    tweets = list(map(lambda data: IncomingTweet(data, identity), timeline))
    tweets.reverse()
    response = BotgleResponse(identity, armed=False)
    testcases = []

    for tweet in tweets:
        logging.info(tweet.text)
        testcases.append(tweet.text)

        if response.condition(tweet):
            try:
                response.respond(tweet)
            except Exception as ex:
                logger.exception(ex)

    # pprint.pprint(testcases)
