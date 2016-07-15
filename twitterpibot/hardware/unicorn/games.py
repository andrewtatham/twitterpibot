import random
from itertools import cycle

from twitterpibot.hardware.unicorn.directions import NORMAL
from twitterpibot.hardware.unicorn.sprites import Particle
from twitterpibot.logic import image_helper


class GameObject(Particle):
    def __init__(self, buffer, rgb):
        super(GameObject, self).__init__(buffer, rgb)

    def iterate(self):
        pass

    def is_collision(self, position):
        return self._position == position


class SnakeHead(GameObject):
    def __init__(self, buffer, rgb):
        super(SnakeHead, self).__init__(buffer, rgb)
        self._direction = random.choice(NORMAL)

    def iterate(self):
        self._position = self._direction.move(self._position, wrap=True)

    def steer(self, snakes, food):
        pass


class RandomSnakeHead(SnakeHead):
    def steer(self, snakes, food):
        r = random.randint(0, 10)
        if r == 0:
            self._direction = self._direction.turn_left()
        elif r == 1:
            self._direction = self._direction.turn_right()


class ShortSightedSnakeHead(SnakeHead):
    def steer(self, snakes, foods):

        straight_position = self._direction.move(self._position, wrap=True)
        left_turn_position = self._direction.turn_left().move(self._position, wrap=True)
        right_turn_position = self._direction.turn_left().move(self._position, wrap=True)

        straight_collision = False
        left_turn_collision = False
        right_turn_collision = False
        left_turn_food = False
        right_turn_food = False

        for snake in snakes:
            straight_collision = straight_collision or snake.is_collision(straight_position, exclude_head=snake == self)
            left_turn_collision = left_turn_collision or snake.is_collision(left_turn_position,
                                                                            exclude_head=snake == self)
            right_turn_collision = right_turn_collision or snake.is_collision(right_turn_position,
                                                                              exclude_head=snake == self)
        for food in foods:
            left_turn_food = left_turn_food or food.is_collision(left_turn_position)
            right_turn_food = right_turn_food or food.is_collision(right_turn_position)

        if straight_collision:
            turn_left = random.randint(0, 1)
            turn_right = not turn_left
            if turn_left and left_turn_collision:
                turn_left = False
            elif turn_right and right_turn_collision:
                turn_left = True
            if turn_left:
                self._direction = self._direction.turn_left()
            else:
                self._direction = self._direction.turn_right()

        elif left_turn_food and not left_turn_collision:
            self._direction = self._direction.turn_left()
        elif right_turn_food and not right_turn_collision:
            self._direction = self._direction.turn_right()
        else:
            r = random.randint(0, 10)
            if r == 0:
                self._direction = self._direction.turn_left()
            elif r == 1:
                self._direction = self._direction.turn_right()

class SnakeSegment(GameObject):
    def __init__(self, buffer, position, rgb):
        super(SnakeSegment, self).__init__(buffer, rgb)
        self._position = position

    def set_rgb(self, rgb):
        self.rgb = rgb


class Snake(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._length = 3
        self.complete = False
        self._hsv = (random.uniform(0.0, 0.75), 1.0, buffer.max_bright)
        self._hsv_alt = (self._hsv[0], 0.9, self._hsv[2])
        self._rgb = image_helper.hsv_to_rgb_alt(self._hsv)
        self._rgb_alt = image_helper.hsv_to_rgb_alt(self._hsv_alt)
        self._colours = cycle([self._rgb, self._rgb_alt])

        self.head = ShortSightedSnakeHead(buffer, self._rgb)

        self._segments = [self.head]

    def iterate(self):

        self._add_segment()
        self.head.iterate()

        if self._length <= len(self._segments):
            last_segment = self._segments[-1:][0]
            self._segments.remove(last_segment)

    def is_collision(self, position, exclude_head):
        if exclude_head:
            segments = self._segments[1:]
        else:
            segments = self._segments

        for segment in segments:
            if segment.is_collision(position):
                return True
        return False

    def clear(self):
        if self.complete:
            for segment in self._segments:
                segment.clear()
        else:
            last_segment = self._segments[-1:][0]
            last_segment.clear()

    def draw(self):

        self.head.draw()

        for segment in self._segments[1:]:
            segment.set_rgb(next(self._colours))
            segment.draw()

    def eat(self, food):
        food.complete = True
        self._length += 1

    def _add_segment(self):
        new_segment = SnakeSegment(self._buffer, self.head._position, self._rgb)
        self._segments.insert(1, new_segment)

    def steer(self, snakes, food):
        self.head.steer(snakes, food)


class FoodPellet(GameObject):
    def __init__(self, buffer):
        hsv = (random.uniform(0.75, 1.0), 1.0, buffer.max_bright)
        rgb = image_helper.hsv_to_rgb_alt(hsv)
        super(FoodPellet, self).__init__(buffer, rgb)


class SnakeGame(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._snakes = []
        self._food = []
        for _ in range(3):
            self.add_snake()
            self.add_food()

    def iterate(self):
        for snake in self._snakes:
            snake.clear()

        for snake in self._snakes:
            snake.steer(self._snakes, self._food)

        for snake in self._snakes:
            snake.iterate()

        self.detect_collisions()

        self.remove_completed_items()

        self.draw()

    def remove_completed_items(self):
        for food in self._food:
            if food.complete:
                self._food.remove(food)
                # self.add_food()
        for snake in self._snakes:
            if snake.complete:
                snake.clear()
                self._snakes.remove(snake)
                self.add_snake()

    def draw(self):
        for food in self._food:
            food.draw()
        for snake in self._snakes:
            snake.draw()

    def detect_collisions(self):
        for snake1 in self._snakes:
            for snake2 in self._snakes:
                if snake1 == snake2:
                    # check for collision with self (exclude head)
                    for snake1segment in snake1._segments[1:]:
                        if snake1.head.is_collision(snake1segment._position):
                            snake1.complete = True
                else:
                    # check for collision with other snake
                    for snake2segment in snake2._segments:
                        if snake1.head.is_collision(snake2segment._position):
                            snake1.complete = True
        for snake in self._snakes:
            for food in self._food:
                if snake.head.is_collision(food._position):
                    snake.eat(food)

    def add_snake(self):
        self._snakes.append(Snake(self._buffer))

    def add_food(self):
        self._food.append(FoodPellet(self._buffer))
