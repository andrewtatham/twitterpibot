import copy
import re
import logging

from twitterpibot.logic import dictionary

logger = logging.getLogger(__name__)
n = 4
rx = re.compile("[\w]+")


class Tile(object):
    def __init__(self, row, col, letters):
        self.row = row
        self.col = col
        self.letters = letters
        self.adjacent_tiles = {}

    def __repr__(self):
        text = '("{letters}",{row},{col})'.format(**self.__dict__)
        if logger.isEnabledFor(logging.DEBUG):
            text += " adj:"
            for letter, tiles in self.adjacent_tiles.items():
                for tile in tiles:
                    text += " {letters} ({row},{col}) ".format(**tile.__dict__)
        return text


class State(object):
    def __init__(self, word):
        self.word = word
        self.tiles = self._parse_tiles(word)
        self.current_tile = None
        self.visited = [[False for _ in range(n)] for _ in range(n)]
        self.path = []

    def found(self):
        return not any(self.tiles)

    def get_next_tile_letters(self):
        tile_letter = self.tiles.pop()
        if tile_letter == "Q":
            # where a Q is not followed by U
            tile_letter += "U"
        return tile_letter

    def __str__(self):
        return "{word} {tiles} {visited}".format(**self.__dict__)

    def is_visited(self, tile):
        return self.visited[tile.row][tile.col]

    def mark_visited(self, tile):
        self.visited[tile.row][tile.col] = True
        self.path.append(tile)

    @staticmethod
    def _parse_tiles(word):
        logging.debug("parsing: %s", word)
        tile_letters = []
        letters = list(word)
        letters.reverse()
        while letters:
            letter = letters.pop()
            if letter == "Q" and letters:

                next_letter = letters.pop()
                if next_letter == "U":
                    # a Q followed by a U
                    letter += next_letter
                    tile_letters.append(letter)
                else:
                    # a Q not followed by a U
                    tile_letters.append(letter)
                    tile_letters.append(next_letter)
            else:
                tile_letters.append(letter)
        tile_letters.reverse()
        logging.debug("tiles: %s", tile_letters)
        return tile_letters


class Tiles(object):
    def __init__(self, board):
        self._tiles_by_letter = {}
        self._tiles_xy = {}
        for this_row in range(n):
            self._tiles_xy[this_row] = {}
            for this_col in range(n):
                this_tile = Tile(this_row, this_col, board[this_row][this_col])
                self._tiles_xy[this_row][this_col] = this_tile
                if this_tile.letters in self._tiles_by_letter:
                    self._tiles_by_letter[this_tile.letters].append(this_tile)
                else:
                    self._tiles_by_letter[this_tile.letters] = [this_tile]

        for this_row in range(n):
            for this_col in range(n):
                moves = []
                if this_row > 0 and this_col > 0:
                    moves.append((-1, -1))  # up left
                if this_row > 0:
                    moves.append((-1, 0))  # up
                if this_row > 0 and this_col < n - 1:
                    moves.append((-1, 1))  # up right
                if this_col > 0:
                    moves.append((0, -1))  # left
                if this_col < n - 1:
                    moves.append((0, 1))  # right
                if this_row < n - 1 and this_col > 0:
                    moves.append((1, -1))  # down left
                if this_row < n - 1:
                    moves.append((1, 0))  # down
                if this_row < n - 1 and this_col < n - 1:
                    moves.append((1, 1))  # down right

                this_tile = self._tiles_xy[this_row][this_col]
                for row_delta, col_delta in moves:
                    next_row = this_row + row_delta
                    next_col = this_col + col_delta
                    adjacent_tile = self._tiles_xy[next_row][next_col]
                    if adjacent_tile.letters in this_tile.adjacent_tiles:
                        this_tile.adjacent_tiles[adjacent_tile.letters].append(adjacent_tile)
                    else:
                        this_tile.adjacent_tiles[adjacent_tile.letters] = [adjacent_tile]

    def can_find(self, word=None, state=None):
        if not state:
            logger.debug("Looking for word {}".format(word))
            state = State(word)

        if state.found():
            logger.debug("Found word {}".format(state.word))
            return state.path

        tile_letter = state.get_next_tile_letters()

        logger.debug("Looking for tile {}".format(tile_letter))

        next_tiles = None
        if state.current_tile:
            if tile_letter in state.current_tile.adjacent_tiles:
                next_tiles = list(filter(lambda tile: not state.is_visited(tile),
                                         state.current_tile.adjacent_tiles[tile_letter]))
            else:
                logger.debug("Could not find adjacent tile {}".format(tile_letter))
                return False
        else:
            if tile_letter in self._tiles_by_letter:
                next_tiles = self._tiles_by_letter[tile_letter]
            else:
                logger.debug("Could not find tile {}".format(tile_letter))

        if next_tiles:
            for next_tile in next_tiles:
                logger.debug("Found tile {}".format(next_tile))
                state_copy = copy.deepcopy(state)
                state_copy.current_tile = next_tile
                state_copy.mark_visited(state_copy.current_tile)
                if self.can_find(state=state_copy):
                    state.path = state_copy.path
                    return state.path
        return False


intros = [
    "THE BOARD:",
    "Boggle Summons You:",
    "TIME FOR BOGGLE:",
    "The mist clears. Time for Boggle:",
    "You see a Boggle board in the distance:",
    "You awaken from a dream of eldritch horrors to find a game before you:",
    "The only thing blocking you from total victory is this Boggle board:",
    "B-O-G-G-L-E",
    "Above you a skywriter dances the path of a Boggle board",
    "Your dreams are haunted by visions of Boggle",
    "I love you. Let's play:",
    "Would you like to play a game of Boggle?",
    "I hear you like to play Boggle",

    "The timer is started! 8 minutes to play!",
    "Warning! Just 3 minutes left",
]


def parse_board(tweet_text):
    for intro in intros:
        if intro in tweet_text:
            tweet_text = tweet_text.replace(intro, "")
            matches = rx.findall(tweet_text)
            if matches and len(matches) >= n * n:
                board = [[None for _ in range(n)] for _ in range(n)]
                for i in range(n * n):
                    board[i // n][i % n] = "".join([chr(ord(c) - 65248) for c in matches[i]]).upper()
                logger.info(board)
                return board

    return None


def solve_board(board):
    candidates = get_candidates(board)
    tiles = Tiles(board)
    solutions = {}
    for candidate in candidates:
        path = tiles.can_find(candidate)
        if path:
            solutions[candidate] = path
    return solutions


def get_candidates(board):
    letters = ""
    for row in board:
        letters += "".join(row)
    candidates = dictionary.get_botgle_candidates(letters)
    return candidates
