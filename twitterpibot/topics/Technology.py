from twitterpibot.topics.Topic import NewsTopic, GoodTopic


class FlyingThings(GoodTopic):
    def __init__(self):
        super(FlyingThings, self).__init__(
            ["Drone", "(quad|hexa?)copter"]
        )


class RaspberryPi(GoodTopic):
    def __init__(self):
        super(RaspberryPi, self).__init__(
            ["rpi", "@Raspberry_Pi", "Raspberry ?Pi", "Pi ?Zero", "raspbian"]
        )


class Python(GoodTopic):
    def __init__(self):
        super(Python, self).__init__(
            ["Python"]
        )


class Arduino(GoodTopic):
    def __init__(self):
        super(Arduino, self).__init__(
            ["Arduino"]
        )


class Git(GoodTopic):
    def __init__(self):
        super(Git, self).__init__(
            ["Git(flow|hub)?"]
        )


class Apple(NewsTopic):
    def __init__(self):
        super(Apple, self).__init__(
            ["Apple", "Mac(intosh|book)", "i(P(a|o)d|phone|tunes|watch)(e?s)?"]
        )


class Microsoft(NewsTopic):
    def __init__(self):
        super(Microsoft, self).__init__(
            ["Microsoft", "Windows", "Bing"]

        )


class Google(NewsTopic):
    def __init__(self):
        super(Google, self).__init__(
            ["Google", "Android", "Chrome", "GMail"]
        )


class Linux(NewsTopic):
    def __init__(self):
        super(Linux, self).__init__(
            ["Linux", "Ubuntu", "Debian", "(Linus) Torvalds"],
            ["Linus"]
        )


class Bots(GoodTopic):
    def __init__(self):
        super(Bots, self).__init__(
            ["bots?", "robots?", "botsummit"]

        )


class APIs(GoodTopic):
    def __init__(self):
        super(APIs, self).__init__(
            ["APIs?", "REST(ful)?","web ?services?"]

        )


class OpenSource(GoodTopic):
    def __init__(self):
        super(OpenSource, self).__init__(
            ["Open Source", "OSS"]

        )


def get():
    return [
        RaspberryPi(),
        Python(),
        Arduino(),
        Git(),
        Apple(),
        Microsoft(),
        Google(),
        Linux(),
        Bots(),
        APIs(),
        OpenSource()
    ]
