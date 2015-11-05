from twitterpibot.twitter.topics.Topic import NewsTopic, GoodTopic


class RaspberryPi(GoodTopic):
    def __init__(self):
        super(RaspberryPi, self).__init__(
            ["Raspberry pi"]
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


class Apple(NewsTopic):
    def __init__(self):
        super(Apple, self).__init__(
            ["Apple", "Mac(intosh|book)", "iP(a|o)d", "iphone"]
        )


class Microsoft(NewsTopic):
    def __init__(self):
        super(Microsoft, self).__init__(
            ["Microsoft", "Windows", "Bing"]

        )


class Google(NewsTopic):
    def __init__(self):
        super(Google, self).__init__(
            ["Google", "Android", "Chrome"]
        )


class Linux(NewsTopic):
    def __init__(self):
        super(Linux, self).__init__(
            ["Linux", "Ubuntu", "Debian", "(Linus) Torvalds"],
            ["Linus"]
        )


def get():
    return [
        RaspberryPi(),
        Python(),
        Arduino(),
        Apple(),
        Microsoft(),
        Google(),
        Linux()
    ]
