import os
import pprint

import feedparser

from twitterpibot.logic import urlhelper, markovhelper,webscraper
from twitterpibot.twitter.topics.Topics import get_topics

andrew_tatham_github_activity = 'https://github.com/andrewtatham.atom'
mark_gelder_blog = "http://markgelder.com/feed/"
helen_frances = "https://helenandfrances.wordpress.com/feed/"
jamie_final_fantasy = "https://fightingfantasyproject.wordpress.com/feed/"

flickr_sunrise_sunset = "https://api.flickr.com/services/feeds/photos_public.gne?tags={tags}&tagmode=any"

google_news = "http://news.google.co.uk/news?cf=all&hl=en&pz=1&ned=uk&output=rss"
bbc_news_magazine = "http://feeds.bbci.co.uk/news/magazine/rss.xml"


# all = [
#     andrew_tatham_github_activity,
#     mark_gelder_blog,
#     helen_frances,
#     jamie_final_fantasy
# ]
# for feed_url in all:
#     print(feed_url)
#     feed = feedparser.parse(feed_url)
#     print(feed["feed"]["title"])
#     for entry in feed["entries"]:
#         print(entry["title"])
#
#     # pprint.pprint(feed)

def get_flickr(**kwargs):
    url = "https://api.flickr.com/services/feeds/photos_public.gne"
    url = urlhelper.parameterise(kwargs, url)
    feed = feedparser.parse(url)
    for entry in feed["entries"]:
        image = {
            "title": entry["title"],
            "image_url": list(filter(lambda link: link["rel"] == "enclosure", entry["links"]))[0]["href"],
            "credit_url": entry["link"]

        }
        pprint.pprint(image)
        print("")

        # pprint.pprint(feed)


def get_sunrise_urls():
    return get_flickr(tags="sunset")


def get_news_stories():
    items = []
    for url in [google_news, bbc_news_magazine]:
        feed = feedparser.parse(url)
        for entry in feed["entries"]:
            topics = get_topics(entry["title"])
            if not topics or topics.reply():
                items.append(entry["title"])
    return items


