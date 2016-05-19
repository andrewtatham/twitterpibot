from twitterpibot.topics.Topic import IgnoreTopic, SpamTopic, GoodTopic


class Lego(GoodTopic):
    def __init__(self):
        super(Lego, self).__init__({"Lego"})


class DecsAndLondon(SpamTopic):
    def __init__(self):
        super(DecsAndLondon, self).__init__({"DecsAndLondon", "#DoItLikeItsLegal"})


class Starbucks(IgnoreTopic):
    def __init__(self):
        super(Starbucks, self).__init__(
            {
                "Pumpkin Spice(d) Latte", "PSL",
                "Red Cups", "(Eggnog|Gingerbread) Latte"
            })


class Nutribullet(IgnoreTopic):
    def __init__(self):
        super(Nutribullet, self).__init__({"NutriBullet(UK)?"})


class Deliveroo(IgnoreTopic):
    def __init__(self):
        super(Deliveroo, self).__init__({"Deliveroo"})


class OtherCorporate(IgnoreTopic):
    def __init__(self):
        super(OtherCorporate, self).__init__({"RoundTeam"})


def get():
    return [
        Lego(),

        Starbucks(),
        DecsAndLondon(),
        Nutribullet(),
        Deliveroo(),
        OtherCorporate()
    ]
