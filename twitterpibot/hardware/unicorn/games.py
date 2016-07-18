import random
import itertools

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

    def clear(self):
        self._buffer.set_pixel(self._position, (0, 0, 0))

    def draw(self):
        self._buffer.set_pixel(self._position, self.rgb)


class SnakeHead(GameObject):
    def __init__(self, buffer, rgb):
        super(SnakeHead, self).__init__(buffer, rgb)
        self._direction = random.choice(NORMAL)

    def iterate(self, wrap):
        self._position = self._direction.move(self._position, wrap=wrap)

    def steer(self, snakes, food, wrap):
        pass


class RandomSnakeHead(SnakeHead):
    def steer(self, snakes, food, wrap):
        r = random.randint(0, 10)
        if r == 0:
            self._direction = self._direction.turn_left()
        elif r == 1:
            self._direction = self._direction.turn_right()


class ShortSightedSnakeHead(SnakeHead):
    def steer(self, snakes, foods, wrap):
        distance_seen = 3

        straight_collision = False
        left_turn_collision = False
        right_turn_collision = False
        straight_food = False
        left_turn_food = False
        right_turn_food = False

        left_turn_direction = self._direction.turn_left()
        right_turn_direction = self._direction.turn_right()

        straight_positions = []
        straight_position = self._position
        for _ in range(distance_seen):
            straight_position = self._direction.move(straight_position, wrap=wrap)
            straight_positions.append(straight_position)

        left_turn_positions = []
        left_turn_position = self._position
        for _ in range(distance_seen):
            left_turn_position = left_turn_direction.move(left_turn_position, wrap=wrap)
            left_turn_positions.append(left_turn_position)

        right_turn_positions = []
        right_turn_position = self._position
        for _ in range(distance_seen):
            right_turn_position = right_turn_direction.move(right_turn_position, wrap=wrap)
            right_turn_positions.append(right_turn_position)

        if not wrap:
            if straight_positions[:1][0].is_off():
                straight_collision = True
            if left_turn_positions[:1][0].is_off():
                left_turn_collision = True
            if right_turn_positions[:1][0].is_off():
                right_turn_collision = True

        for snake in snakes:
            for straight_position in straight_positions[:1]:
                straight_collision = straight_collision or \
                                     snake.is_collision(straight_position, exclude_head=snake == self)
            for left_turn_position in left_turn_positions[:1]:
                left_turn_collision = left_turn_collision or \
                                      snake.is_collision(left_turn_position, exclude_head=snake == self)
            for right_turn_position in right_turn_positions[:1]:
                right_turn_collision = right_turn_collision or \
                                       snake.is_collision(right_turn_position, exclude_head=snake == self)

        for food in foods:
            for straight_position in straight_positions:
                straight_food = straight_food or food.is_collision(straight_position)
            for left_turn_position in left_turn_positions:
                left_turn_food = left_turn_food or food.is_collision(left_turn_position)
            for right_turn_position in right_turn_positions:
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
        elif straight_food:
            pass
        elif left_turn_food and not left_turn_collision:
            self._direction = self._direction.turn_left()
        elif right_turn_food and not right_turn_collision:
            self._direction = self._direction.turn_right()
        else:
            r = random.randint(0, 64)
            if r == 0 and not left_turn_collision:
                self._direction = self._direction.turn_left()
            elif r == 1 and not right_turn_collision:
                self._direction = self._direction.turn_right()


class SnakeSegment(GameObject):
    def __init__(self, buffer, position, rgb):
        super(SnakeSegment, self).__init__(buffer, rgb)
        self._position = position

    def set_rgb(self, rgb):
        self.rgb = rgb


class Snake(object):
    def __init__(self, buffer, h, length):
        self._buffer = buffer
        self._length = length
        self.complete = False
        self._hsv = (h, 1.0, buffer.max_bright)
        self._poisonous = random.randint(0, 9) == 0
        if self._poisonous:
            self._hsv_alt = (image_helper.h_delta(self._hsv[0], random.uniform(0.1, 0.3)), 1.0, self._hsv[2])
        else:
            self._hsv_alt = (self._hsv[0], random.uniform(0.7, 0.9), self._hsv[2])

        self._rgb = image_helper.hsv_to_rgb_alt(self._hsv)
        self._rgb_alt = image_helper.hsv_to_rgb_alt(self._hsv_alt)

        self.head = ShortSightedSnakeHead(buffer, self._rgb)

        self._segments = [self.head]

    def iterate(self, wrap):

        self._add_segment()
        self.head.iterate(wrap)

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
        colours = itertools.cycle([self._rgb_alt, self._rgb, self._rgb])
        for segment in self._segments[1:]:
            segment.set_rgb(next(colours))
            segment.draw()

    def eat(self, food):
        food.complete = True
        self._length += 1

    def _add_segment(self):
        new_segment = SnakeSegment(self._buffer, self.head._position, self._rgb)
        self._segments.insert(1, new_segment)

    def steer(self, snakes, food, wrap):
        self.head.steer(snakes, food, wrap)


class FoodPellet(GameObject):
    def __init__(self, buffer):
        # hsv = (random.uniform(0.75, 1.0), 1.0, buffer.max_bright)
        # rgb = image_helper.hsv_to_rgb_alt(hsv)
        rgb = (buffer.max_bright, buffer.max_bright, buffer.max_bright)
        super(FoodPellet, self).__init__(buffer, rgb)


class SnakeGameOptions(object):
    def __init__(self, n_snakes=1, n_food=1, replenish_food=False, snake_length=3, wrap=False):
        self.n_snakes = n_snakes
        self.n_food = n_food
        self.replenish_food = replenish_food
        self.snake_length = snake_length
        self.wrap = wrap


class SnakeGame(object):
    def __init__(self, buffer, options):
        self._buffer = buffer
        self._options = options
        self.h = random.uniform(0.0, 1.0)
        self._snakes = []
        self._food = []
        for _ in range(self._options.n_snakes):
            self.add_snake()
        for _ in range(self._options.n_food):
            self.add_food()

    def iterate(self):
        for snake in self._snakes:
            snake.clear()

        for snake in self._snakes:
            snake.steer(self._snakes, self._food, self._options.wrap)

        for snake in self._snakes:
            snake.iterate(self._options.wrap)

        self.detect_collisions()

        self.remove_completed_items()

        self.draw()

    def remove_completed_items(self):
        for food in self._food:
            if food.complete:
                self._food.remove(food)
                if self._options.replenish_food:
                    self.add_food()
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

            if not self._options.wrap:
                for snake1segment in snake1._segments:
                    if snake1segment._position.is_off():
                        snake1.complete = True

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
        self.h = image_helper.h_delta(self.h, random.uniform(0.2, 0.9))
        self._snakes.append(Snake(self._buffer, h=self.h, length=self._options.snake_length))

    def add_food(self):
        self._food.append(FoodPellet(self._buffer))
