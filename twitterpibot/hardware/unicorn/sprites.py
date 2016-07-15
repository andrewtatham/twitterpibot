import itertools
import random

from twitterpibot.hardware.unicorn.directions import DIAGONALS, Position


class Particle(object):
    def __init__(self, buffer, rgb, trails=False):
        self._buffer = buffer
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        self._position = Position(x, y)
        self.rgb = rgb
        self.complete = False
        self._trails = trails

    def clear(self):
        self.draw(clear=True)

    def draw(self, clear=False):
        if not clear or clear and not self._trails:
            self._buffer.pixel_delta(clear, self._position, self.rgb)


class Raindrop(Particle):
    def __init__(self, buffer, rgb, direction, trails):
        super(Raindrop, self).__init__(buffer, rgb, trails)
        self._direction = direction
        self._position = self._direction.start_position()

    def clear(self):
        if not self._trails:
            super(Raindrop, self).clear()

    def draw(self, clear=False):
        if clear and not self._trails:
            self._buffer.set_pixel(self._position, (0, 0, 0))
        else:
            self._buffer.set_pixel(self._position, self.rgb)

    def iterate(self):
        self._position = self._direction.move(self._position)
        self.complete = self._position.is_off()


class ExpandingParticle(Particle):
    def __init__(self, buffer, rgb):
        super(ExpandingParticle, self).__init__(buffer, rgb)
        self.r = 0

    def iterate(self):
        self.r += 1
        if self.r > 8:
            self.complete = True


class Firework(ExpandingParticle):
    def draw(self, clear=False):
        for xy in itertools.product([-self.r, 0, self.r], [-self.r, 0, self.r]):
            if self.r == 0 or xy != (0, 0):
                x = self._position.x + xy[0]
                y = self._position.y + xy[1]
                position = Position(x, y)
                self._buffer.pixel_delta(clear, position, self.rgb)


class Square(ExpandingParticle):
    def draw(self, clear=False):
        for x in range(self._position.x - self.r, self._position.x + self.r + 1):
            self._buffer.pixel_delta(clear, Position(x, self._position.y - self.r), self.rgb)
            self._buffer.pixel_delta(clear, Position(x, self._position.y + self.r), self.rgb)

        for y in range(self._position.y - self.r + 1, self._position.y + self.r + 1):
            self._buffer.pixel_delta(clear, Position(self._position.x - self.r, y), self.rgb)
            self._buffer.pixel_delta(clear, Position(self._position.x + self.r, y), self.rgb)


class BouncingBall(Particle):
    def __init__(self, buffer, rgb):
        super(BouncingBall, self).__init__(buffer, rgb, trails=True)
        self._bounce_count = 0
        self._direction = random.choice(DIAGONALS)
        self._position = self._direction.start_position()

    def iterate(self):
        new_direction = self._direction.bounce(self._position)
        if new_direction:
            self._direction = new_direction
            self._bounce_count += 1
            self.complete = self._bounce_count >= 5

        self._position = self._direction.move(self._position)
