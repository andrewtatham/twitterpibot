import datetime
import random
import re
import pprint

from twitterpibot.logic import weather

screen_name = "BBCWeatherBot"

bbc_weather_bot_fail_rx = re.compile("Sorry|We found more than one location with that name")
bbc_weather_bot_rx = re.compile(
    "(?P<temp>temperatures (up to|as low as) [\d]+°C),( (?P<blah1>[\w\s]+))? and (?P<blah2>[\w\s]+)\.")
temperature_rx = re.compile(
    "temperatures (?P<direction>up to|as low as) (?P<degrees>[\d]+)°C")
bbc_phrases = {}
bbc_emoji = {}

say = ["apparently", "it says here"]
templates = []
templates.extend(map(lambda t: t + " '{}'", say))
templates.extend(map(lambda t: "'{}' " + t, say))

for weather_type in weather.weather_types:
    if weather_type._bbc_phrases:
        for phrase in weather_type._bbc_phrases:
            interestingness = weather_type._bbc_phrases[phrase]
            bbc_phrases[phrase] = interestingness
            if weather_type._emoji:
                bbc_emoji[phrase] = weather_type._emoji


def _parse(text):
    if bbc_weather_bot_fail_rx.search(text):
        return None
    match = bbc_weather_bot_rx.search(text)
    if match:
        return list(match.groupdict().values())
    else:
        return None


def _temperature(temperature_text):
    temp_match = temperature_rx.search(temperature_text)
    if temp_match:
        degrees = int(temp_match.group("degrees"))
        direction = temp_match.group("direction")

        low, avg, high = weather.average_high_low_temperatures[datetime.datetime.today().month]
        if degrees > 25:
            phrase = weather.hot.get_phrase()
            return phrase, 5
        elif degrees <= 0:
            phrase = weather.freeze.get_phrase()
            return phrase, 5
        if direction == "up to" and high < degrees:
            diff = degrees - high
            phrase = weather.warm.get_phrase()
            return phrase, diff
        elif direction == "as low as" and degrees < low:
            diff = low - degrees
            phrase = weather.cold.get_phrase()
            return phrase, diff

    return None, None


def get_bbc_weather_bot_text(tweet_text):
    phrases = _parse(tweet_text)

    interesting_phrases = []
    new_phrases = []
    emoji = ""
    if phrases:
        for phrase in phrases:
            if phrase:
                if "temperatures" in phrase:

                    temperature_phrase, temperature_interestingness = _temperature(phrase)
                    if temperature_phrase and temperature_interestingness:
                        interesting_phrases.append((temperature_phrase, temperature_interestingness))

                elif phrase in bbc_phrases:
                    interestingness = bbc_phrases[phrase]
                    interesting_phrases.append((phrase, interestingness))
                    if phrase in bbc_emoji:
                        emoji += random.choice(bbc_emoji[phrase])
                else:
                    new_phrases.append(phrase)

        interesting_phrases.sort(key=lambda t: t[1])

        phrase = interesting_phrases.pop()[0]
        template = random.choice(templates)
        text = template.format(phrase) + " " + emoji

        return text, new_phrases
    else:
        return None, None


if __name__ == '__main__':
    ordered = list(bbc_phrases.items())
    ordered.sort(key=lambda t: t[1])
    pprint.pprint(ordered)
    pprint.pprint(bbc_emoji)

if __name__ == '__main__':
    import identities

    identity = identities.AndrewTathamPiIdentity(None)
    for tweet in identity.twitter.get_user_timeline(screen_name=screen_name, count=200):
        tweet_text = tweet["text"]

        reply1, new_phrases = get_bbc_weather_bot_text(tweet_text)
        if reply1:
            print(tweet_text)
            if new_phrases:
                print("new_phrases:" + str(new_phrases))
            print(reply1)
            reply2 = weather.get_weather_response(reply1)
            print(reply2)
            reply3 = weather.get_weather_response(reply2)
            print(reply3)
            print("-")
