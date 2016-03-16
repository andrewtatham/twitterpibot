import random
from urllib.parse import quote_plus

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.logic import googlehelper
from twitterpibot.processing.Conversational import HelloWords
from twitterpibot.responses.Response import Response
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet

leeds = {
    'id': '6863fd050de21120',
    'place_type': 'city',
    'country_code': 'GB',
    'attributes': {},
    'country': 'United Kingdom',
    'bounding_box': {
        'coordinates': [[[-1.706057, 53.736369],
                         [-1.706057, 53.867543],
                         [-1.424923, 53.867543],
                         [-1.424923, 53.736369]]],
        'type': 'Polygon'},
    'full_name': 'Leeds, England',
    'name': 'Leeds',
    'url': 'https://api.twitter.com/1.1/geo/id/6863fd050de21120.json'}

sightseeing = {
    "The Great Barrier Reef, Queensland, Australia",
    "Pyramids of Giza, Egypt",
    "Stonehenge, Amesbury, England",
    "Salar De Uyuni, Bolivia",
    "The Grand Canyon, Arizona, USA",
    "Antelope Canyon, Arizona, USA",
    "Easter Island, Rapa Nui, Chile",
    "Reed Flute Caves, China",
    "The Great Wall of China, China",
    "Plitvice Lakes National Park, Croatia",

}


class Location(object):
    def __init__(self, place=None, coordinates=None,
                 latitude=None, longitude=None):

        self.full_name = None
        if place:
            self.full_name = place["full_name"]

        self.longitude = None
        self.latitude = None
        if coordinates:
            self.longitude = coordinates(0)
            self.latitude = coordinates(1)
        elif longitude and latitude:
            self.longitude = longitude
            self.latitude = latitude

    def __str__(self):
        return "{full_name} ({longitude},{latitude})".format(**self.__dict__)

    def get_search_string(self):
        if self.longitude and self.latitude:
            return self.get_latlng_string()
        elif self.full_name:
            return quote_plus(self.full_name)

    def get_address_string(self):
        if self.full_name:
            return quote_plus(self.full_name)

    def get_latlng_string(self):
        if self.longitude and self.latitude:
            return "{latitude},{longitude}".format(**self.__dict__)

    def get_display_name(self):
        if self.full_name:
            return self.full_name
        elif self.longitude and self.latitude:
            return self.get_latlng_string()


def get_random_location_by_name():
    return Location(place={
        'full_name': random.choice(sightseeing)
    })


def get_random_location_by_latlng():
    return Location(latitude=round(random.uniform(-90, 90), 6),
                    longitude=round(random.uniform(-180, 180), 6))


class LocationScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=random.randint(1, 2))

    def on_run(self):
        location = get_random_location_by_name()
        location = googlehelper.geocode(location)
        file_paths = googlehelper.get_location_images(location, "location")

        text = ".@" + self.identity.converse_with + " " + random.choice(HelloWords) + \
               " I'm at " + location.get_display_name()
        self.identity.twitter.send(OutgoingTweet(text=text, location=location, file_paths=file_paths))


class LocationResponse(Response):
    def condition(self, inbox_item):
        return (
                   super(LocationResponse, self).mentioned_reply_condition(inbox_item)
                   # or super(LocationResponse, self).unmentioned_reply_condition(inbox_item)
                   or super(LocationResponse, self).testing_reply_condition(inbox_item)
               ) and inbox_item.is_tweet and inbox_item.location

    def respond(self, inbox_item):
        if inbox_item.location:
            file_paths = googlehelper.get_location_images(inbox_item.location, inbox_item.status_id)
            text = random.choice(HelloWords)
            self.identity.twitter.reply_with(inbox_item, text=text, file_paths=file_paths)
