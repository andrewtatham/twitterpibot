import logging
import pprint
import random
from twitterpibot.incoming.IncomingTweet import IncomingTweet

from twitterpibot.logic import botgle_artist
from twitterpibot.logic.botgle_solver import parse_board, solve_board
from twitterpibot.outgoing import OutgoingDirectMessage
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.responses.Response import Response

logger = logging.getLogger(__name__)


class BotgleGame(object):
    def __init__(self):
        self.board = None
        self.solution = None

    def board_recieved(self, board):
        if not self.board or self.board != board:
            self.board = board
            self.solution = solve_board(self.board)
            return self.solution

    def game_over(self):
        if self.board and self.solution:
            image = botgle_artist.make(self.board, self.solution)
            self.board = None
            self.solution = None
            return image
        else:
            return None


class BotgleResponse(Response):
    def __init__(self, identity):
        super(BotgleResponse, self).__init__(identity)
        self._game = BotgleGame()

    def condition(self, inbox_item):
        return inbox_item.is_tweet and inbox_item.sender.screen_name == "Botgle"

    def respond(self, inbox_item):
        board = parse_board(inbox_item.text)

        # GAME OVER! SCORES:
        # Next game in 6 hours!
        # Warning! Just 3 minutes left
        # The timer is started! 8 minutes to play!

        descriptions = [
            "I call it: %s",
            "piece titled: %s",
            "title: %s",
        ]
        if "GAME OVER" in inbox_item.text:
            image = self._game.game_over()
            if image:
                text = "@andrewtatham "
                text += random.choice(descriptions) % image["name"]
                file_paths = [image["file_path"]]
                self.identity.twitter.send(OutgoingTweet(text=text, file_paths=file_paths))

        elif board:
            solutions = self._game.board_recieved(board)
            if solutions:
                logger.info("%s words found..." % len(solutions))

                words = list(solutions)
                words.sort(key=len)
                words = words[-12:]
                words.reverse()

                text = "@andrewtatham "
                text += ("%s words found " % len(solutions))
                text += " ".join(words)

                self.identity.twitter.send(
                    OutgoingDirectMessage.OutgoingDirectMessage(text=text, screen_name="andrewtatham"))


if __name__ == '__main__':
    import main
    logging.basicConfig()

    identity = main.AndrewTathamPiIdentity(None)
    timeline = identity.twitter.get_user_timeline(screen_name="botgle", exclude_replies=True, count=200)
    tweets = list(map(lambda data: IncomingTweet(data, identity), timeline))
    tweets.reverse()
    response = BotgleResponse(identity)
    for tweet in tweets:
        print(tweet.text)

        if response.condition(tweet):
            response.respond(tweet)


