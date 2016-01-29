import os
from twitterpibot.twitter.topics import Topics
from twitterpibot.twitter import TwitterHelper

import datetime
import logging

try:
    from functools import reduce
except NameError:
    pass

UK_WOEID = 23424975
US_WOEID = 23424977

logger = logging.getLogger(__name__)

_trending = []
_updated = None



class TrendingTopic(object):
    def __init__(self, topic_text):
        self.text = topic_text
        self.topics = None
        logger.info('Determining topics for ' + self.text)
        # self.topics = Topics.get_topics(topic_text)
        # if self.topics:
        #     logger.info('Determined topics for ' + self.text + ' to be ' + str(self.topics))
        # else:
        logger.info('Getting tweets for ' + self.text)
        topic_tweets = TwitterHelper.search(topic_text)
        if topic_tweets:
            tweets_text = reduce(lambda t1, t2: t1 + os.linesep + t2, map(lambda t: t['text'], topic_tweets))
            tweets_text = ''.join([i if ord(i) < 128 else ' ' for i in tweets_text])
            logger.info('Determining topics for ' + tweets_text)
            self.topics = Topics.get_topics(tweets_text)
            if self.topics:
                logger.info('Determined topics for ' + self.text + ' to be ' + str(self.topics))

    def __str__(self):
        txt = self.__class__.__name__ + ': ' + self.text
        if self.topics:
            txt += ': ' + str(self.topics)

        return txt


def _update():
    global _trending
    global _updated

    topics_text = TwitterHelper.get_trending_topics_for([UK_WOEID, US_WOEID])
    _trending = list(map(lambda topic_text: TrendingTopic(topic_text), topics_text))
    _updated = datetime.datetime.now()


def get():
        if _updated:
            delta = datetime.datetime.now() - _updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
            if mins > 45:
                _update()
        else:
            _update()
        return _trending
