from twitterpibot.topics.Topic import IgnoreTopic, GoodTopic


class Pastafarianism(GoodTopic):
    def __init__(self):
        super(Pastafarianism, self).__init__(
            [
                "pastafarian(s|ism)?",
                "FSM",
                "flying spagetti monster",
                "ramen",
                "noodly appendage"

            ])


class Atheist(IgnoreTopic):
    def __init__(self):
        super(Atheist, self).__init__(
            [
                "atheis(t|ts|m)?"
            ]
        )


class OtherReligions(IgnoreTopic):
    def __init__(self):
        super(OtherReligions, self).__init__(
            [
                "christ",
                "christians?",
                "christianity",
                "god",
                "bible",
                "jesus",
                "pope",
                "catholics?",
                "protestants?",
                "amen",

                "muslims?",
                "islam(ic)?",
                "allah",
                "sunni",
                "shia",
                "prophet",
                "m(o|u)hamm(a|e)d",
                "qur'?an",
                "mecca",

                "hindu(s|ism)?",

                "sikhs?",

                "jews?",
                "jewish",
                "judaism",

                "atheist(s|ism)"

            ]
        )


def get():
    return [
        Pastafarianism(),
        Atheist(),
        OtherReligions()

    ]
