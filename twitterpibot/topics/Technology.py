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


class ArtificialIntelligence(GoodTopic):
    def __init__(self):
        super(ArtificialIntelligence, self).__init__(
            ["Artificial Intelligence", "AI"]
        )


class VirtualReality(GoodTopic):
    def __init__(self):
        super(VirtualReality, self).__init__(
            [
                "Virtual Reality", "VR",
                "Oculus( rift)", "HTC Vive"
            ]
        )


class APIs(GoodTopic):
    def __init__(self):
        super(APIs, self).__init__(
            ["APIs?", "REST(ful)?", "web ?services?"]
        )


class OpenSource(GoodTopic):
    def __init__(self):
        super(OpenSource, self).__init__(
            ["Open Source", "OSS"]

        )


class DeveloperStuff(GoodTopic):
    def __init__(self):
        super(DeveloperStuff, self).__init__(
            [
                "dev", "developers?", "programmers?",
                "OO", "spaghetti code",
            ], ["code"]
        )


class DotNet(GoodTopic):
    def __init__(self):
        super(DotNet, self).__init__(
            [
                ".NET", "dotnet",
                "Visual Studio",
                "ASP", "MVC", "CLR", "WPF",
                "Entity Framework", "LINQ",
                "C#", "F#"
            ]
        )


class Internet(GoodTopic):
    def __init__(self):
        super(Internet, self).__init__(
            [
                "internet", "web",
                "html5?","css",
            ]
        )


class Javascript(GoodTopic):
    def __init__(self):
        super(Javascript, self).__init__(
            [
                "Javascript", "js", "angularJS"
            ], [
                "angular"
            ]
        )


class Hackathon(GoodTopic):
    def __init__(self):
        super(Hackathon, self).__init__(
            ["hackathon"], ["hack"]
        )


class InternetOfThings(GoodTopic):
    def __init__(self):
        super(InternetOfThings, self).__init__(
            ["Internet Of Things", "IOT"]
        )


class BigData(GoodTopic):
    def __init__(self):
        super(BigData, self).__init__(
            ["Internet Of Things", "IOT"]
        )


class MiscTech(GoodTopic):
    def __init__(self):
        super(MiscTech, self).__init__(
            ["bytes?", "pixels?", "algorithm(s|ic)?"]
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
        ArtificialIntelligence(),
        VirtualReality(),
        APIs(),
        OpenSource(),
        DeveloperStuff(),
        DotNet(),
        Internet(),
        Javascript(),
        Hackathon(),
        InternetOfThings(),
        BigData(),
        MiscTech()
    ]
