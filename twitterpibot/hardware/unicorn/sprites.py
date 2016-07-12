import random


class Particle(object):
    def __init__(self, buffer, x, y, rgb):
        self._buffer = buffer
        self.x = x
        self.y = y
        self.rgb = rgb
        self.complete = False

    def clear(self):
        self.draw(clear=True)

    def draw(self, clear=False):
        pass


class Raindrop(Particle):
    def __init__(self, buffer, rgb, direction, trails=False):
        self._direction = direction
        if self._direction == "up":
            x = 0
            y = random.randint(0, 7)
        elif self._direction == "right":
            x = random.randint(0, 7)
            y = 0
        elif self._direction == "down":
            x = 7
            y = random.randint(0, 7)
        elif self._direction == "left":
            x = random.randint(0, 7)
            y = 7
        else:
            raise Exception("Invalid direction")
        self._trails = trails
        super(Raindrop, self).__init__(buffer, x, y, rgb)

    def clear(self):
        if not self._trails:
            super(Raindrop, self).clear()

    def draw(self, clear=False):
        if clear:
            self._buffer.set_pixel(self.x, self.y, (0, 0, 0))
        else:
            self._buffer.set_pixel(self.x, self.y, self.rgb)

    def iterate(self):
        if self._direction == "up":
            self.x += 1
        elif self._direction == "right":
            self.y += 1
        elif self._direction == "down":
            self.x -= 1
        elif self._direction == "left":
            self.y -= 1

        if self._direction == "up" and self.x > 7 \
                or self._direction == "right" and self.y > 7 \
                or self._direction == "down" and self.x < 0 \
                or self._direction == "left" and self.y < 0:
            self.complete = True


class ExpandingParticle(Particle):
    def __init__(self, buffer, rgb):
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        super(ExpandingParticle, self).__init__(buffer, x, y, rgb)
        self.r = 0

    def iterate(self):
        self.r += 1
        if self.r > 16:
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
