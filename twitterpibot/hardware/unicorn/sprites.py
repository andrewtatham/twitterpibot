import random


class Direction(object):
    up = "up"
    down = "down"
    left = "left"
    right = "right"

    up_left = ["U", "L"]
    up_right = ["U", "R"]
    down_left = ["D", "L"]
    down_right = ["D", "R"]

    diagnals = [
        up_left,
        up_right,
        down_left,
        down_right]


class Particle(object):
    def __init__(self, buffer, x, y, rgb, trails=False):
        self._buffer = buffer
        self.x = x
        self.y = y
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
        self._direction = direction
        if self._direction == Direction.up:
            x = 0
            y = random.randint(0, 7)
        elif self._direction == Direction.right:
            x = random.randint(0, 7)
            y = 0
        elif self._direction == Direction.down:
            x = 7
            y = random.randint(0, 7)
        elif self._direction == Direction.left:
            x = random.randint(0, 7)
            y = 7
        else:
            raise Exception("Invalid direction")
        super(Raindrop, self).__init__(buffer, x, y, rgb, trails)

    def clear(self):
        if not self._trails:
            super(Raindrop, self).clear()

    def draw(self, clear=False):
        if clear and not self._trails:
            self._buffer.set_pixel(self.x, self.y, (0, 0, 0))
        else:
            self._buffer.set_pixel(self.x, self.y, self.rgb)

    def iterate(self):
        if self._direction == Direction.up:
            self.x += 1
        elif self._direction == Direction.right:
            self.y += 1
        elif self._direction == Direction.down:
            self.x -= 1
        elif self._direction == Direction.left:
            self.y -= 1

        if self._direction == Direction.up and self.x > 7 \
                or self._direction == Direction.right and self.y > 7 \
                or self._direction == Direction.down and self.x < 0 \
                or self._direction == Direction.left and self.y < 0:
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


class BouncingBall(Particle):
    def __init__(self, buffer, rgb):
        self._bounce_count = 0
        self._direction = random.choice(Direction.diagnals)
        x, y = self._set_starting_position()
        super(BouncingBall, self).__init__(buffer, x, y, rgb)

    def _set_starting_position(self):
        coin_toss = random.randint(0, 1) == 0
        if self._direction == Direction.up_left:
            if coin_toss:
                return self._start_from_bottom()
            else:
                return self._start_from_right()
        elif self._direction == Direction.up_right:
            if coin_toss:
                return self._start_from_bottom()
            else:
                return self._start_from_left()
        elif self._direction == Direction.down_left:
            if coin_toss:
                return self._start_from_top()
            else:
                return self._start_from_right()
        elif self._direction == Direction.down_right:
            if coin_toss:
                return self._start_from_top()
            else:
                return self._start_from_left()
        else:
            raise Exception("Invalid direction")

    def _start_from_top(self):
        x = random.randint(0, 7)
        y = 7
        return x, y

    def _start_from_bottom(self):
        x = random.randint(0, 7)
        y = 0
        return x, y

    def _start_from_left(self):
        x = 0
        y = random.randint(0, 7)
        return x, y

    def _start_from_right(self):
        x = 7
        y = random.randint(0, 7)
        return x, y

    def iterate(self):
        self._bounce()
        self._move()

    def _bounce(self):
        has_bounced = False
        if self.y == 0:
            if self._direction == Direction.down_left:
                self._direction = Direction.up_left
                has_bounced = True
            elif self._direction == Direction.down_right:
                self._direction = Direction.up_right
                has_bounced = True
        elif self.y == 7:
            if self._direction == Direction.up_left:
                self._direction = Direction.down_left
                has_bounced = True
            elif self._direction == Direction.up_right:
                self._direction = Direction.down_right
                has_bounced = True

        if self.x == 0:
            if self._direction == Direction.up_left:
                self._direction = Direction.up_right
                has_bounced = True
            elif self._direction == Direction.down_left:
                self._direction = Direction.down_right
                has_bounced = True
        elif self.x == 7:
            if self._direction == Direction.up_right:
                self._direction = Direction.up_left
                has_bounced = True
            elif self._direction == Direction.down_right:
                self._direction = Direction.down_left
                has_bounced = True

        if has_bounced:
            self._bounce_count += 1

        if self._bounce_count > 5:
            self.complete = True

    def _move(self):
        if self._direction == Direction.up_right or self._direction == Direction.down_right:
            self.x += 1
        elif self._direction == Direction.up_left or self._direction == Direction.down_left:
            self.x -= 1

        if self._direction == Direction.up_left or self._direction == Direction.up_right:
            self.y += 1
        elif self._direction == Direction.down_left or self._direction == Direction.down_right:
            self.y -= 1
