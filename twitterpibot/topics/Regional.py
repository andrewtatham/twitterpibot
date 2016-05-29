from twitterpibot.logic.regional import yorkshire_places
from twitterpibot.topics.Topic import GoodTopic, IgnoreTopic


class Leeds(GoodTopic):
    def __init__(self):
        super(Leeds, self).__init__(
            [
                "Leeds",
                "Aberford",
                "Adel",
                "Aireborough",
                "Alwoodley",
                "Armley",
                "Austhorpe",
                "Bardsey cum Rigton",
                "Bardsey",
                "Barwick-in-Elmet",
                "Beck Hill",
                "Beckett Park",
                "Beeston",
                "Beeston Hill",
                "Belle Isle",
                "Blenheim",
                "Bramhope",
                "Bramley",
                "Bramstan",
                "Burley",
                "Burmantofts",
                "Buslingthorpe",
                "Carlton",
                "Chapel Allerton",
                "Chapeltown",
                "Churwell",
                "Colton",
                "Cookridge",
                "Cottingley",
                "Cranmer Bank",
                "Cross Gates",
                "Cross Green",
                "East End Park",
                "East Keswick",
                "Far Headingley",
                "Farnley",
                "Fearnville",
                "Garforth",
                "Gildersome",
                "Gipton",
                "Gledhow",
                "Great Preston",
                "Guiseley",
                "Halton",
                "Halton Moor",
                "Harehills",
                "Harewood",
                "Hawksworth",
                "Hawksworth",
                "Headingley",
                "Holbeck",
                "Holbeck Urban Village",
                "Holt Park",
                "Horsforth",
                "Hunslet",
                "Hyde Park",
                "Ireland Wood",
                "Killingbeck",
                "Kippax",
                "Kirkstall",
                "Knowsthorpe",
                "Lawnswood",
                "Ledsham",
                "Leeds city centre",
                "Lincoln Green",
                "Little London",
                "Lovell Park",
                "Mabgate",
                "Manston",
                "Meanwood",
                "Methley",
                "Micklefield",
                "Mickletown",
                "Middleton",
                "Miles Hill",
                "Moor Allerton",
                "Moor Grange",
                "Moorside",
                "Moortown",
                "Morley",
                "Oakwood",
                "Osmondthorpe",
                "Oulton",
                "Potternewton",
                "Potterton",
                "Quarry Hill",
                "Rawdon",
                "Richmond Hill",
                "Rodley",
                "Rothwell",
                "Roundhay",
                "Scarcroft",
                "Scholes",
                "Scott Hall",
                "Seacroft",
                "Shadwell",
                "Sheepscar",
                "Stourton",
                "Swarcliffe",
                "Swillington",
                "Swinnow",
                "Thorner",
                "Tinshill",
                "Weardley",
                "Weetwood",
                "West Park",
                "Whinmoor",
                "Whitkirk",
                "Wike",
                "Woodhouse",
                "Woodlesford",
                "Wortley",
                "Wykebeck",
            ]
        )


class Yorkshire(GoodTopic):
    def __init__(self):
        super(Yorkshire, self).__init__(
            ["Yorkshire"],
            yorkshire_places

        )


class London(IgnoreTopic):
    def __init__(self):
        super(London, self).__init__(
            ["London", "LDN"]
        )


class Europe(IgnoreTopic):
    def __init__(self):
        super(Europe, self).__init__(
            ["Europe", "European", "EU"]
        )


def get():
    return [
        Leeds(),
        Yorkshire(),
        London(),
        Europe()
    ]
