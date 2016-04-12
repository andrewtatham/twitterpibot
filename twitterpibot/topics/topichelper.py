import logging

from twitterpibot.topics import Daily, Monthly, Annual, Politics, Sport, Entertainment, Celebrity, News, \
    Technology, Regional, Spam, Competitions
from twitterpibot.topics import religion
from twitterpibot.topics import Corporate

logger = logging.getLogger(__name__)

try:
    from functools import reduce
except NameError:
    pass

_topics = []
_topics.extend(Daily.get())
_topics.extend(Monthly.get())
_topics.extend(Annual.get())
_topics.extend(Politics.get())
_topics.extend(Celebrity.get())
_topics.extend(Sport.get())
_topics.extend(Entertainment.get())
_topics.extend(News.get())
_topics.extend(Corporate.get())
_topics.extend(Technology.get())
_topics.extend(Regional.get())
_topics.extend(Spam.get())
_topics.extend(Competitions.get())
_topics.extend(religion.get())

for topic in _topics:
    logger.debug("Topic %s definite: %s",
                 topic.__str__(),
                 topic.definite_rx
                 )
    if topic.possible_rx:
        logger.debug("Topic %s possible: %s",
                     topic.__str__(),
                     topic.possible_rx
                     )


class Topics(object):
    def __init__(self, topics_list):
        self._topics_list = topics_list

    def retweet(self):
        bools = map(lambda t: bool(t['retweet']), self._topics_list)
        return reduce(lambda t1, t2: t1 and t2, bools)

    def stream(self):
        bools = map(lambda t: bool(t['stream']), self._topics_list)
        return reduce(lambda t1, t2: t1 and t2, bools)

    def reply(self):
        bools = map(lambda t: bool(t['reply']), self._topics_list)
        return reduce(lambda t1, t2: t1 and t2, bools)

    def spam(self):
        bools = map(lambda t: bool(t['spam']), self._topics_list)
        return reduce(lambda t1, t2: t1 or t2, bools)

    def __str__(self):
        return str(self._topics_list)


def get_topics(text):
    results = map(lambda t: t.condition(text), _topics)
    matching_topics = list(filter(_has_matches, results))
    if 0 < len(matching_topics) <= 3:
        return Topics(sorted(matching_topics, key=_score, reverse=True))
    else:
        return None


def _has_matches(result):
    return result and ("definite_matches" in result and result["definite_matches"]
                       or "possible_matches" in result and result["possible_matches"])


def _score(result):
    score = 0
    if "definite_matches" in result:
        score += len(result["definite_matches"]) * 10
    if "possible_matches" in result:
        score += len(result["possible_matches"])
    return score
