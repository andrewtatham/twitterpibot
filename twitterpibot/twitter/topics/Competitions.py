from twitterpibot.twitter.topics.Topic import DontCareTopic


class RetweetForXFavouriteForY(DontCareTopic):
    def __init__(self):
        super(RetweetForXFavouriteForY, self).__init__([
            # RT to Win
            "(RT|Retweet|chance|follow).*(to|2).*win",

            # RT/Fav voting
            "(RT|Retweet).*(Fav|Like)",
            "(Fav|Like).*(RT|Retweet)",

        ])


def get():
    return [
        RetweetForXFavouriteForY()
    ]
