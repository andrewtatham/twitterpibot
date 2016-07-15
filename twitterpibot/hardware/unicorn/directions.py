import random


class Position(object):
    def __init__(self, x, y, wrap=False):
        self.x = x
        self.y = y
        if wrap:
            if self.x < 0: self.x = 7
            if self.x > 7: self.x = 0
            if self.y < 0: self.y = 7
            if self.y > 7: self.y = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def is_off(self):
        return self.x > 7 or self.y > 7 \
               or self.x < 0 or self.y < 0


class Direction(object):
    def move(self, position, wrap=False):
        return position

    def start_position(self):
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        return Position(x, y)

    def bounce(self, position):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass




class DiagonalDirection(Direction):
    def __init__(self):
        super(Direction, self).__init__()
        self.vertical = None
        self.horizontal = None

    def move(self, position, wrap=False):
        position = self.vertical.move(position, wrap)
        position = self.horizontal.move(position, wrap)
        return position

    def start_position(self):
        coin_toss = random.randint(0, 1) == 0
        if coin_toss:
            return self.vertical.start_position()
        else:
            return self.horizontal.start_position()

    def bounce(self, position):
        pass


class Up(Direction):
    def move(self, position, wrap=False):
        return Position(position.x, position.y + 1, wrap)

    def start_position(self):
        x = random.randint(0, 7)
        y = 0
        return Position(x, y)

    def bounce(self, position):
        if position.y == 7:
            return Down()

    def turn_left(self):
        return Left()

    def turn_right(self):
        return Right()


class Down(Direction):
    def move(self, position, wrap=False):
        return Position(position.x, position.y - 1, wrap)

    def start_position(self):
        x = random.randint(0, 7)
        y = 7
        return Position(x, y)

    def bounce(self, position):
        if position.y == 0:
            return Up()

    def turn_left(self):
        return Right()

    def turn_right(self):
        return Left()


class Left(Direction):
    def move(self, position, wrap=False):
        return Position(position.x - 1, position.y, wrap)

    def start_position(self):
        x = 7
        y = random.randint(0, 7)
        return Position(x, y)

    def bounce(self, position):
        if position.x == 0:
            return Right()

    def turn_left(self):
        return Down()

    def turn_right(self):
        return Up()


class Right(Direction):
    def move(self, position, wrap=False):
        return Position(position.x + 1, position.y, wrap)

    def start_position(self):
        x = 0
        y = random.randint(0, 7)
        return Position(x, y)

    def bounce(self, position):
        if position.x == 7:
            return Left()

    def turn_left(self):
        return Up()

    def turn_right(self):
        return Down()


class UpLeft(DiagonalDirection):
    def __init__(self):
        super(UpLeft, self).__init__()
        self.horizontal = Left()
        self.vertical = Up()

    def bounce(self, position):
        if position.x == 0 and position.y == 7:
            return DownRight()
        elif position.x == 0:
            return UpRight()
        elif position.y == 7:
            return DownLeft()


class UpRight(DiagonalDirection):
    def __init__(self):

        super(UpRight, self).__init__()
        self.horizontal = Right()
        self.vertical = Up()

    def bounce(self, position):
        if position.x == 7 and position.y == 7:
            return DownLeft()
        elif position.x == 7:
            return UpLeft()
        elif position.y == 7:
            return DownRight()


class DownLeft(DiagonalDirection):
    def __init__(self):
        super(DownLeft, self).__init__()
        self.horizontal = Left()
        self.vertical = Down()

    def bounce(self, position):
        if position.x == 0 and position.y == 0:
            return UpRight()
        elif position.x == 0:
            return DownRight()
        elif position.y == 0:
            return UpLeft()


class DownRight(DiagonalDirection):
    def __init__(self):
        super(DownRight, self).__init__()
        self.horizontal = Right()
        self.vertical = Down()

    def bounce(self, position):
        if position.x == 7 and position.y == 0:
            return UpLeft()
        elif position.x == 7:
            return DownLeft()
        elif position.y == 0:
            return UpRight()


UP = Up()
DOWN = Down()
LEFT = Left()
RIGHT = Right()

NORMAL = [
    UP,
    DOWN,
    LEFT,
    RIGHT
]

UP_LEFT = UpLeft()
UP_RIGHT = UpRight()
DOWN_LEFT = DownLeft()
DOWN_RIGHT = DownRight()

DIAGONALS = [
    UP_LEFT,
    UP_RIGHT,
    DOWN_LEFT,
    DOWN_RIGHT]
