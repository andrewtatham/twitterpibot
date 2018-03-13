from twitterpibot.logic import eggpuns
from twitterpibot.topics.Topic import GoodTopic, IgnoreTopic


class GoodFood(GoodTopic):
    def __init__(self):
        super(GoodFood, self).__init__({
            "peanut butter",
            "cookies?",
            "ice cream",
            "realbread",
            "pizza",

        })


class Vegetarianism(IgnoreTopic):
    def __init__(self):
        super(Vegetarianism, self).__init__({
            "Vegetarian(s|ism)?"
        })


class Veganism(IgnoreTopic):
    def __init__(self):
        super(Veganism, self).__init__({
            "Vegan(s|ism)"
        })


class Eggs(GoodTopic):
    def __init__(self):
        super(Eggs, self).__init__(eggpuns.gif_search_words)


def get():
    return [
        GoodFood(),
        Vegetarianism(),
        Veganism(),
        Eggs()
    ]
