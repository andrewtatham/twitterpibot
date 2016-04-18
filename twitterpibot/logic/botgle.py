import logging
import pprint
import random
import re

from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.logic import botgle_solver, botgle_artist
from twitterpibot.logic.conversation import hello_words
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.responses.Response import Response

logger = logging.getLogger(__name__)
descriptions = [
    "this piece is titled: %s",
    "piece titled: %s",
    "title: %s",
]
frame_request = [
    "please can you put this in a frame for me?",
    "do your thang",
]
# todo manage files / make collage?
played_rx = re.compile("@(?P<screen_name>[\w_]+) plays (?P<words>[\w\s]+)")


class BotgleGame(object):
    def __init__(self, identity):
        self.board_in_progress = None
        self.solution = None
        self.identity = identity
        self.played_words = {}

    def read_tweet(self, inbox_item):
        retval = {}
        board = botgle_solver.parse_board(inbox_item.text)
        if board:
            self._on_board(board, retval)
        elif self.is_played_words(inbox_item):
            self.on_played_word(inbox_item)
        elif self._is_game_over(inbox_item):
            self._on_game_over(retval)
        elif self._is_next_game_in_x_minutes(inbox_item):
            self._on_next_game_in_x_minutes(retval)
        elif self._is_next_game_in_x_hours(inbox_item):
            self._on_next_game_in_x_hours(retval)
        return retval

    def _on_board(self, board, retval):
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

    def _on_game_over(self, retval):
        if self.board_in_progress and self.solution:
            image = botgle_artist.make(self.board_in_progress, self.solution, self.identity.screen_name)
            retval["image"] = image
        # todo follow mentioned users?
        if self.played_words:
            for screen_name, words in self.played_words.items():
                logger.info("{} {}".format(screen_name, words))

        self.board_in_progress = None
        self.solution = None

    def _on_next_game_in_x_hours(self, retval):
        # retval["text"] = random.choice([
        #     "[buys paint]",
        #     "[buys canvas]",
        #     "[buys brushes]",
        #     "[cleans brushes]",
        #     "[sleeps]",
        #     "[contemplates]"
        # ])
        pass

    def _on_next_game_in_x_minutes(self, retval):
        # retval["text"] = random.choice([
        #     "[mixes paint]",
        #     "[fetches easel]",
        #     "[gets canvas]",
        #     "[prepares canvas]",
        # ])
        pass

    def _is_game_over(self, inbox_item):
        return "GAME OVER" in inbox_item.text

    def _is_next_game_in_x_minutes(self, inbox_item):
        return "Boggle in" in inbox_item.text and "minutes" in inbox_item.text

    def _is_next_game_in_x_hours(self, inbox_item):
        # todo regex
        return "Next game in" in inbox_item.text \
               and "hours" in inbox_item.text

    def is_played_words(self, inbox_item):
        return " plays " in inbox_item.text

    def on_played_word(self, inbox_item):
        match = played_rx.search(inbox_item.text)
        screen_name = str(match.groupdict()["screen_name"])
        words = set([word for word in match.groupdict()["words"].split(" ") if word])
        if screen_name not in self.played_words:
            self.played_words[screen_name] = set()
        self.played_words[screen_name].update(words)
        # todo find words on board, make picture if following?


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
                    self._reply_with_image(image, inbox_item)
                    if random.randint(0, 9) == 0:
                        self._update_profile_picture(image)
                    if random.randint(0, 9) == 0:
                        self._get_image_framed(image)
                
            elif "solutions" in response:
                if "text" in response:
                    text = response["text"]
                    self._tweet(text)
                solutions = response["solutions"]
                if solutions:
                    self._solution_found(solutions)

            elif "text" in response:
                text = response["text"]
                self._tweet(text)

    def _tweet(self, text):
        if self._armed:
            self.identity.twitter.send(OutgoingTweet(text=text))
        else:
            logger.info(text)

    def _solution_found(self, solutions):
        words = list(solutions)
        words.sort(key=len)
        words = words[-10:]
        words.reverse()
        text = ""
        text += ("%s words found: " % len(solutions))
        text += " ".join(words)
        # if self._armed:
        #     # self.identity.twitter.send(
        #     #     OutgoingDirectMessage.OutgoingDirectMessage(text=text, screen_name="andrewtatham"))
        # else:
        logger.info(text)

    def _reply_with_image(self, image, inbox_item):
        text = ""
        text += random.choice(descriptions) % image["name"]
        file_paths = [image["file_path"]]
        if self._armed:
            text = ".@Botgle " + text
            self.identity.twitter.send(OutgoingTweet(text=text, file_paths=file_paths,
                                                     in_reply_to_id_str=inbox_item.id_str))
        else:
            logger.info("tweets " + text + " " + str(file_paths))

    def _update_profile_picture(self, image):

        file_path = image["file_path"]
        if self._armed:
            self.identity.twitter.update_profile_image(file_path=file_path)
        else:
            logger.info("updates profile image " + file_path)

    def _get_image_framed(self, image):
        text = random.choice(hello_words)
        text += " @ShouldFrameIt "
        text += random.choice(frame_request)
        file_paths = [image["file_path"]]
        if self._armed:
            text = " " + text
            self.identity.twitter.send(OutgoingTweet(text=text, file_paths=file_paths))
        else:
            logger.info("tweets " + text + " " + str(file_paths))


if __name__ == '__main__':
    import identities

    logging.basicConfig(level=logging.INFO)

    identity = identities.BotgleArtistIdentity(None)
    timeline = identity.twitter.get_user_timeline(screen_name="botgle", count=50)
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
