import random

from twitterpibot.hardware.unicorn.directions import NORMAL
from twitterpibot.hardware.unicorn.sprites import Particle


class GameObject(Particle):
    def __init__(self, buffer, rgb):
        super(GameObject, self).__init__(buffer, rgb)

    def iterate(self):
        pass


class SnakeHead(GameObject):
    def __init__(self, buffer):
        super(SnakeHead, self).__init__(buffer, rgb=(0, buffer.max_bright, 0))
        self._direction = random.choice(NORMAL)

    def iterate(self):
        r = random.randint(0, 10)
        if r == 0:
            self._direction = self._direction.turn_left()
        elif r == 1:
            self._direction = self._direction.turn_right()

        self._direction.move(self)

        if self.x < 0: self.x = 7
        if self.x > 7: self.x = 0
        if self.y < 0: self.y = 7
        if self.y > 7: self.y = 0


class SnakeSegment(GameObject):
    def __init__(self, buffer, x, y, direction):
        super(SnakeSegment, self).__init__(buffer, rgb=(0, int(buffer.max_bright / 2), 0))
        self._direction = direction
        self.x = x
        self.y = y


class Snake(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self.head = SnakeHead(buffer)
        self._segments = [self.head]
        self._length = 2
        self.complete = False

    def iterate(self):

        if self._length >= len(self._segments):
            last_segment = self._segments[-1:][0]
            self._segments.remove(last_segment)

        self._add_segment()
        self.head.iterate()

        for segment in self._segments:
            if segment != self.head and segment.x == self.head.x and segment.y == self.head.y:
                self.complete = True

    def clear(self):
        if self.complete:
            for segment in self._segments:
                segment.clear()
        else:
            last_segment = self._segments[-1:][0]
            last_segment.clear()

    def draw(self):
        for segment in self._segments:
            segment.draw()

    def eat(self, food):
        print("NOM")
        food.complete = True
        self._length += 1

    def _add_segment(self):
        new_segment = SnakeSegment(self._buffer, self.head.x, self.head.y, self.head._direction)
        self._segments.insert(1, new_segment)


class FoodPellet(GameObject):
    def __init__(self, buffer):
        super(FoodPellet, self).__init__(buffer, rgb=(buffer.max_bright, 0, 0))


class SnakeGame(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._snakes = []
        self._food = []
        self.add_snake()
        self.add_food()

    def iterate(self):
        for snake in self._snakes:
            snake.clear()

        for snake in self._snakes:
            snake.iterate()

        for snake in self._snakes:
            for food in self._food:
                if snake.head.x == food.x and snake.head.y == food.x:
                    snake.eat(food)

        for food in self._food:
            if food.complete:
                self._food.remove(food)
                # self.add_food()

        for snake in self._snakes:
            if snake.complete:
                snake.clear()
                self._snakes.remove(snake)
                self.add_snake()

        for food in self._food:
            food.draw()

        for snake in self._snakes:
            snake.draw()

    def add_snake(self):
        self._snakes.append(Snake(self._buffer))

    def add_food(self):
        self._food.append(FoodPellet(self._buffer))
