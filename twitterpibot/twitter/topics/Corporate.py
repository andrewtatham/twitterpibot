from twitterpibot.twitter.topics.Topic import DontCareTopic, SpamTopic


class DecsAndLondon(SpamTopic):
    def __init__(self):
        super(DecsAndLondon, self).__init__({"DecsAndLondon", "#DoItLikeItsLegal"})


class Starbucks(DontCareTopic):
    def __init__(self):
        super(Starbucks, self).__init__(
            {
                "Pumpkin Spice(d) Latte", "PSL",
                "Red Cups", "(Eggnog|Gingerbread) Latte"
            })


class Nutribullet(DontCareTopic):
    def __init__(self):
        super(Nutribullet, self).__init__({"NutriBullet(UK)?"})


class Deliveroo(DontCareTopic):
    def __init__(self):
        super(Deliveroo, self).__init__({"Deliveroo"})


class OtherCorporate(DontCareTopic):
    def __init__(self):
        super(OtherCorporate, self).__init__({"RoundTeam"})


def get():
    return [
        Starbucks(),
        DecsAndLondon(),
        Nutribullet(),
        Deliveroo(),
        OtherCorporate()
    ]
