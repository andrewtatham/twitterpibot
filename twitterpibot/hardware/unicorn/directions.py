import random


class Direction(object):
    def move(self, item):
        pass

    def start_position(self, item):
        item.x = random.randint(0, 7)
        item.y = random.randint(0, 7)

    def bounce(self, item):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass


class DiagnalDirection(Direction):
    def __init__(self):
        super(Direction, self).__init__()
        self.vertical = None
        self.horizontal = None

    def move(self, item):
        self.vertical.move(item)
        self.horizontal.move(item)

    def start_position(self, item):
        coin_toss = random.randint(0, 1) == 0
        if coin_toss:
            self.vertical.start_position(item)
        else:
            self.horizontal.start_position(item)

    def bounce(self, item):
        self.vertical.bounce(item)
        self.horizontal.bounce(item)


class Up(Direction):
    def move(self, item):
        item.y += 1

    def start_position(self, item):
        item.x = random.randint(0, 7)
        item.y = 0

    def bounce(self, item):
        if item.y == 7:
            return Down()

    def turn_left(self):
        return Left()

    def turn_right(self):
        return Right()


class Down(Direction):
    def move(self, item):
        item.y -= 1

    def start_position(self, item):
        item.x = random.randint(0, 7)
        item.y = 7

    def bounce(self, item):
        if item.y == 0:
            return Up()

    def turn_left(self):
        return Right()

    def turn_right(self):
        return Left()


class Left(Direction):
    def move(self, item):
        item.x -= 1

    def start_position(self, item):
        item.x = 7
        item.y = random.randint(0, 7)

    def bounce(self, item):
        if item.x == 0:
            return Right()

    def turn_left(self):
        return Down()

    def turn_right(self):
        return Up()


class Right(Direction):
    def move(self, item):
        item.x += 1

    def start_position(self, item):
        item.x = 0
        item.y = random.randint(0, 7)

    def bounce(self, item):
        if item.x == 7:
            return Left()

    def turn_left(self):
        return Up()

    def turn_right(self):
        return Down()


class UpLeft(DiagnalDirection):
    def __init__(self):
        super(UpLeft, self).__init__()
        self.horizontal = Left()
        self.vertical = Up()

    def bounce(self, item):
        if item.x == 0 and item.y == 7:
            return DownRight()
        elif item.x == 0:
            return UpRight()
        elif item.y == 7:
            return DownLeft()


class UpRight(DiagnalDirection):
    def __init__(self):

        super(UpRight, self).__init__()
        self.horizontal = Right()
        self.vertical = Up()

    def bounce(self, item):
        if item.x == 7 and item.y == 7:
            return DownLeft()
        elif item.x == 7:
            return UpLeft()
        elif item.y == 7:
            return DownRight()


class DownLeft(DiagnalDirection):
    def __init__(self):
        super(DownLeft, self).__init__()
        self.horizontal = Left()
        self.vertical = Down()

    def bounce(self, item):
        if item.x == 0 and item.y == 0:
            return UpRight()
        elif item.x == 0:
            return DownRight()
        elif item.y == 0:
            return UpLeft()


class DownRight(DiagnalDirection):
    def __init__(self):
        super(DownRight, self).__init__()
        self.horizontal = Right()
        self.vertical = Down()

    def bounce(self, item):
        if item.x == 7 and item.y == 0:
            return UpLeft()
        elif item.x == 7:
            return DownLeft()
        elif item.y == 0:
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

DIAGNALS = [
    UP_LEFT,
    UP_RIGHT,
    DOWN_LEFT,
    DOWN_RIGHT]
