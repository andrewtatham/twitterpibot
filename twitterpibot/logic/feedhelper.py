import pprint

import feedparser

andrew_tatham_github_activity = 'https://github.com/andrewtatham.atom'
mark_gelder_blog = "http://markgelder.com/feed/"
helen_frances = "https://helenandfrances.wordpress.com/feed/"
jamie_final_fantasy = "https://fightingfantasyproject.wordpress.com/feed/"

all = [
    andrew_tatham_github_activity,
    mark_gelder_blog,
    helen_frances,
    jamie_final_fantasy
]
for feed_url in all:
    print(feed_url)
    feed = feedparser.parse(feed_url)
    print(feed["feed"]["title"])
    for entry in feed["entries"]:
        print(entry["title"])

    # pprint.pprint(feed)

