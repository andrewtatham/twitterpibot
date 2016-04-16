import logging
import random
import re
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.logic import emojihelper
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet

screen_name = "BBCWeatherBot"
fail_rx = re.compile("Sorry|We found more than one location with that name")
rx = re.compile("(?P<temp>temperatures (up to|as low as) [\d]+°C),( (?P<blah1>[\w\s]+))? and (?P<blah2>[\w\s]+)\.")

logger = logging.getLogger(__name__)


class WeatherScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=7, minute=random.randint(0, 59))

    def on_run(self):
        tweet_id = self.identity.twitter.send(OutgoingTweet(text="@" + screen_name + " Leeds Today"))
        self.identity.conversations.track_replies(tweet_id=tweet_id, response=self.on_response)

    def on_response(self, inbox_item):
        if inbox_item.sender.screen_name == screen_name:

            emoji = self.get_emoji(inbox_item)

            parts = self.parse(inbox_item.text)
            if parts:
                logger.info(str(parts))

                self.identity.twitter.send(OutgoingDirectMessage(text=inbox_item.text + " -> " + str(parts)))

                say = ["apparently", "it says here"]
                templates = []
                templates.extend(map(lambda t: t + " {}", say))
                templates.extend(map(lambda t: "{} " + t, say))

                part = random.choice(parts)

                if "rain" in inbox_item.text:
                    part += emojihelper.umbrella_with_rain_drops

                text = ".@" + self.identity.converse_with + " " + random.choice(templates).format(part)

                if emoji:
                    text += emoji

                self.identity.twitter.quote_tweet(inbox_item=inbox_item, text=text)

    def get_emoji(self, inbox_item):
        emoji = ""
        phrases = {
            "sunshine": [
                emojihelper.sun_with_face,
                emojihelper.black_sun_with_rays,
                emojihelper.smiling_face_with_sunglasses,
            ],
            "clear skies": [
                emojihelper.sun_with_face,
                emojihelper.black_sun_with_rays,
                emojihelper.sunflower,
            ],
            "sunny intervals": [
                emojihelper.sun_behind_cloud,
            ],
            "partial cloud": [
                emojihelper.sun_behind_cloud,
            ],
            "white cloud": [
                emojihelper.cloud
            ],
            "grey cloud": [
                emojihelper.cloud
            ],

            "light rain": [
                emojihelper.thunder_cloud_and_rain,
                emojihelper.droplet,
                emojihelper.closed_umbrella
            ],
            "light rain showers": [
                emojihelper.thunder_cloud_and_rain,
                emojihelper.droplet,
                emojihelper.rainbow,
                emojihelper.umbrella

            ],
            "heavy rain showers": [
                emojihelper.umbrella_with_rain_drops,
                emojihelper.cloud_with_rain,
                emojihelper.rain,
                emojihelper.rainbow,
            ],
            "heavy rain": [
                emojihelper.umbrella_with_rain_drops,
                emojihelper.rain,

            ],

            "a little wind": [
                emojihelper.wind_chime,
                emojihelper.leaf_fluttering_in_wind,
            ],
            "a strong breeze": [
                emojihelper.wind_blowing_face,
            ],
        }
        for phrase in phrases:
            if phrase in inbox_item.text:
                emoji += random.choice(phrases[phrase])

        return emoji

    @staticmethod
    def parse(tweet_text):
        if fail_rx.search(tweet_text):
            return None
        match = rx.search(tweet_text)
        if match:
            return list(match.groupdict().values())
        else:
            return None


if __name__ == '__main__':
    import identities

    identity = identities.AndrewTathamPiIdentity(None)
    phrases = set()
    for tweet in identity.twitter.get_user_timeline(screen_name=screen_name, count=200):
        text = tweet["text"]
        parsed = WeatherScheduledTask.parse(text)

        print("(\"" + text + "\", " + str(parsed) + "),")
        if parsed:
            for phrase in parsed:
                if phrase and "temperatures" not in phrase:
                    phrases.add(phrase)
    for phrase in phrases:
        print(phrase)
