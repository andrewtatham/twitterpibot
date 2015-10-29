from twitterpibot.twitter import TwitterHelper
from multiprocessing import Lock
import datetime

UK_WOEID = 23424975
US_WOEID = 23424977
_trending = []
_lock = Lock()
_updated = None


class TrendingTopic(object):
    pass



def get():
    with _lock:

        if _updated:
            delta = datetime.datetime.now() - _updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
            if mins > 15:
                _update()
        else:
            _update()
        return _trending


def _update():
    global _trending
    global _updated
    _trending = TwitterHelper.GetTrendingTopicsFor([UK_WOEID, US_WOEID])
    _updated = datetime.datetime.now()
