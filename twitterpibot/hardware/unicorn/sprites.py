import random

from twitterpibot.hardware.unicorn.directions import DIAGNALS


class Particle(object):
    def __init__(self, buffer, rgb, trails=False):
        self._buffer = buffer
        self.x = random.randint(0, 7)
        self.y = random.randint(0, 7)
        self.rgb = rgb
        self.complete = False
        self._trails = trails

    def clear(self):
        self.draw(clear=True)

    def draw(self, clear=False):
        if not clear or clear and not self._trails:
            self._buffer.pixel_delta(clear, self.x, self.y, self.rgb)


class Raindrop(Particle):
    def __init__(self, buffer, rgb, direction, trails):
        super(Raindrop, self).__init__(buffer, rgb, trails)
        self._direction = direction
        self._direction.start_position(self)

    def clear(self):
        if not self._trails:
            super(Raindrop, self).clear()

    def draw(self, clear=False):
        if clear and not self._trails:
            self._buffer.set_pixel(self.x, self.y, (0, 0, 0))
        else:
            self._buffer.set_pixel(self.x, self.y, self.rgb)

    def iterate(self):
        self._direction.move(self)
        self.complete = self.x > 7 or self.y > 7 \
                        or self.x < 0 or self.y < 0


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
        self._buffer.pixel_delta(clear, self.x + self.r, self.y, self.rgb)
        self._buffer.pixel_delta(clear, self.x - self.r, self.y, self.rgb)
        self._buffer.pixel_delta(clear, self.x, self.y + self.r, self.rgb)
        self._buffer.pixel_delta(clear, self.x, self.y - self.r, self.rgb)
        self._buffer.pixel_delta(clear, self.x + self.r, self.y + self.r, self.rgb)
        self._buffer.pixel_delta(clear, self.x - self.r, self.y - self.r, self.rgb)
        self._buffer.pixel_delta(clear, self.x - self.r, self.y + self.r, self.rgb)
        self._buffer.pixel_delta(clear, self.x + self.r, self.y - self.r, self.rgb)


class Square(ExpandingParticle):
    def draw(self, clear=False):
        for x in range(self.x - self.r, self.x + self.r + 1):
            self._buffer.pixel_delta(clear, x, self.y - self.r, self.rgb)
            self._buffer.pixel_delta(clear, x, self.y + self.r, self.rgb)

        for y in range(self.y - self.r + 1, self.y + self.r + 1):
            self._buffer.pixel_delta(clear, self.x - self.r, y, self.rgb)
            self._buffer.pixel_delta(clear, self.x + self.r, y, self.rgb)


class BouncingBall(Particle):
    def __init__(self, buffer, rgb):
        super(BouncingBall, self).__init__(buffer, rgb)
        self._bounce_count = 0
        self._direction = random.choice(DIAGNALS)
        self._direction.start_position(self)

    def iterate(self):
        new_direction = self._direction.bounce(self)
        if new_direction:
            self._direction = new_direction
            self._bounce_count += 1
            self.complete = self._bounce_count >= 5

        self._direction.move(self)
