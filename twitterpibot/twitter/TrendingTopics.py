from twitterpibot.twitter.topics import Topics
from twitterpibot.twitter import TwitterHelper
from multiprocessing import Lock
import datetime

UK_WOEID = 23424975
US_WOEID = 23424977

_trending = []
_updated = None
_lock = Lock()

class TrendingTopic(object):
    def __init__(self, topic_text, topic):
        self.text = topic_text
        self.topic = topic

    def __str__(self):
        return self.text


def _update():
    global _trending
    global _updated

    topics_text = TwitterHelper.GetTrendingTopicsFor([UK_WOEID, US_WOEID])
    _trending = list(map(lambda topic_text: TrendingTopic(topic_text, Topics.get_topics(topic_text)), topics_text))
    _updated = datetime.datetime.now()


def get():
    with _lock:
        if _updated:
            delta = datetime.datetime.now() - _updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
            if mins > 45:
                _update()
        else:
            _update()
        return _trending



