import random
from twitterpibot.twitter.topics import Daily
from twitterpibot.twitter.topics import Annual
from twitterpibot.twitter.topics import Celebrity
from twitterpibot.twitter.topics import Politics
from twitterpibot.twitter.topics import Sport

_topics = []
_topics.extend(Daily.get())
_topics.extend(Annual.get())
_topics.extend(Politics.get())
_topics.extend(Celebrity.get())
_topics.extend(Sport.get())


def get_topic(text):
    for topic in _topics:
        if topic.condition(text):
            return topic
    return None
