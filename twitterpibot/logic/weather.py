import random
import re

from twitterpibot.logic import emojihelper, phrase_generator


class WeatherType(object):
    def __init__(self, phrases, rx, emoji, bbc_phrases=None):
        self._phrases = phrases
        self._rx = re.compile(rx, re.IGNORECASE)
        self._emoji = emoji
        self._bbc_phrases = bbc_phrases

    def is_match(self, text):
        return self._rx and self._rx.search(text)

    def get_phrase(self):
        if self._phrases:
            phrase = phrase_generator.generate_phrase(self._phrases)
            if self._emoji:
                phrase + " " + random.choice(self._emoji)

            return phrase


hot = WeatherType(
    rx="hot|heatwave|boiling|scorch(er|ing)|stifling|sweltering",
    phrases=[
        "it's crackin' flags",
        "Looks like we’re in for a hot one",
        "It's a scorcher",
        "We’re having quite a heatwave",
        "it's (boiling|scorching|stifling|sweltering)",
        "Schorchio!"

        "What dreadful hot weather we have! It keeps me in a continual state of inelegance"
    ],
    emoji=[
        emojihelper.thermometer,
        emojihelper.hot_pepper,

        emojihelper.beach_with_umbrella,
        emojihelper.bikini,
        emojihelper.t_shirt,
        emojihelper.ice_cream,
        emojihelper.shaved_ice,
        emojihelper.sunflower,
        emojihelper.sun_with_face,
        emojihelper.black_sun_with_rays
    ])

warm = WeatherType(
    rx="warm",
    phrases=[
        "Ooh it's a bit warm out"

    ],
    emoji=[
        emojihelper.beach_with_umbrella,
        emojihelper.bikini,
        emojihelper.t_shirt,
        emojihelper.ice_cream,
        emojihelper.shaved_ice,
        emojihelper.sunflower,
        emojihelper.sun_with_face,
        emojihelper.black_sun_with_rays
    ])

cold = WeatherType(
    rx="cold|chill",
    phrases=[
        "Take a jacket – it’s a bit chilly out there"

        "The coldest winter I ever spent was a summer in San Francisco"
    ],
    emoji=[
        emojihelper.face_with_cold_sweat,
        emojihelper.face_with_open_mouth_and_cold_sweat
    ])

freeze = WeatherType(
    rx="freeze|frost|ice",
    phrases=[
        "Colder than a witch's tit",
        "Jack Frost has visited",
        "enough to freeze the balls off a brass monkey"
    ],
    emoji=[
        emojihelper.ice_skate,
        emojihelper.ice_hockey_stick_and_puck,

        emojihelper.snowflake,
        emojihelper.snowman,
        emojihelper.cloud_with_snow,
        emojihelper.snowman_without_snow
    ]
)
snow = WeatherType(
    rx="snow",
    phrases=[
        "A lot of people like snow. I find it to be an unnecessary freezing of water",
        "When snow falls, nature listens",
        "The first fall of snow is not only an event, it is a magical event. You go to bed in one kind of world and wake up in another quite different",
        "When I no longer thrill to the first snow of the season, I'll know I'm growing old",
        "Snowflakes are kisses from heaven",
        "The snow doesn’t give a soft white damn whom it touches",
        "Silently, like thoughts that come and go, the snowflakes fall, each one a gem",
        "Where does the white go when the snow melts?",
        "Snowflakes are one of nature’s most fragile things, but just look what they can do when they stick together",
        "Snowmen fall from heaven... unassembled",
        "When it snows, you have two choices: shovel or make snow angels",
        "Look up at the miracle of the falling snow,—the air a dizzy maze of whirling, eddying flakes, noiselessly transforming the world, the exquisite crystals dropping in ditch and gutter, and disguising in the same suit of spotless livery all objects upon which they fall",
    ],
    emoji=[
        emojihelper.snowboarder,
        emojihelper.snowflake,
        emojihelper.snowman,
        emojihelper.cloud_with_snow,
        emojihelper.snowman_without_snow
    ])
# todo hail = WeatherType()
# todo sleet = WeatherType()
storm = WeatherType(
    rx="storm|thunder|lightning",
    emoji=[
        emojihelper.thunder_cloud_and_rain,
        emojihelper.cloud_with_lightning,
        emojihelper.high_voltage_sign
    ],
    phrases=[
        "a storm is brewing",
        "in the quiet before the storm",
        "a storm in a teacup",

        "Any proverbs about weather are doubly true during a storm"
    ])

# todo fog = WeatherType(rx="mist/fog")
# todo gales = WeatherType(rx="gales/hurricane/tornado")

# todo flood = WeatherType(rx="flooding")

sunny = WeatherType(

    bbc_phrases={"clear skies": 1, "sunny intervals": 2, "sunshine": 3},
    rx="sun|sunny|sunshine|bright", emoji=[
        emojihelper.sun_with_face,
        emojihelper.black_sun_with_rays,
        emojihelper.smiling_face_with_sunglasses,
        emojihelper.sunflower,
        emojihelper.dark_sunglasses
    ],
    phrases=[
        "I think the sun is trying to come out",

        "To love and be loved is to feel the sun from both sides",
        "Three things cannot be long hidden: the sun, the moon, and the truth",
        "When the sun is shining I can do anything; no mountain is too high, no trouble too difficult to overcome",
        "Hope is like the sun, which, as we journey toward it, casts the shadow of our burden behind us",
        "Keep your face to the sunshine and you cannot see a shadow",
        "A flower cannot blossom without sunshine, and man cannot live without love",
        "Just living is not enough... one must have sunshine, freedom, and a little flower",
        "Summer means happy times and good sunshine. It means going to the beach, going to Disneyland, having fun",
        "A day without sunshine is like, you know, night",
        "Keep your face always toward the sunshine - and shadows will fall behind you",
        "What sunshine is to flowers, smiles are to humanity. These are but trifles, to be sure; but scattered along life's pathway, the good they do is inconceivable",
        "Anyone's life truly lived consists of work, sunshine, exercise, soap, plenty of fresh air, and a happy contented spirit",
        "I don't complain when it's sunny",
    ])

rainy = WeatherType(

    bbc_phrases={"light rain showers": 2, "light rain": 3, "heavy rain showers": 4, "heavy rain": 5},
    rx="rain|showers|downpour|drizzle|precipitation",
    emoji=[
        emojihelper.droplet,
        emojihelper.cloud_with_rain,

        emojihelper.umbrella,
        emojihelper.closed_umbrella,
        emojihelper.umbrella_with_rain_drops,
    ],
    phrases=[
        "it's raining cats and dogs",
        "it's raining, it's pouring, the old man is snoring",
        "It’s bucketing down",
        "Don’t forget your umbrella",
        "Here's that rainy day you've been saving for",
        "The heavens have opened",
        "its gonna rain on your parade"
        "Rain, rain go away; come back another day",
        "Rain before seven, fine by eleven",

        "I like people who smile when it’s raining",
        "Rainbows apologize for angry skies",
        "Let the rain kiss you. Let the rain beat upon your head with silver liquid drops. Let the rain sing you a lullaby",
        "When halo rings Moon or Sun, rain's approaching on the run",
        "Remember even though the outside world might be raining, if you keep on smiling the sun will soon show its face and smile back at you",
        "The best thing one can do when it's raining is to let it rain",
        "Don't take your toys inside just because it's raining",
        "One thing I love about being back is English rain. I love it. To me, those are reassuringly English things. I love it when it rains.",
        "The shortest period of time lies between the minute you put some money away for a rainy day and the unexpected arrival of rain",
        "You have to accept the storms and the rainy days and the things in life that you sometimes don't want to face",
        "Let the rain kiss you. Let the rain beat upon your head with silver liquid drops. Let the rain sing you a lullaby",
        "Tears of joy are like the summer raindrops pierced by sunbeams",
        "The way I see it, if you want the rainbow, you gotta put up with the rain",
        "Rain is grace; rain is the sky descending to the earth; without rain, there would be no life",
        "And when it rains on your parade, look up rather than down. Without the rain, there would be no rainbow",
        "I think fish is nice, but then I think that rain is wet, so who am I to judge?",
        "If the rain spoils our picnic, but saves a farmer's crop, who are we to say it shouldn't rain?",
        "Remember even though the outside world might be raining, if you keep on smiling the sun will soon show its face and smile back at you",
        "Anyone who says sunshine brings happiness has never danced in the rain",
        "Some people feel the rain — others just get wet",
        "Rain; Whose soft architectural hands have power to cut stones, and chisel to shapes of grandeur the very mountains",
        "Many a man curses the rain that falls upon his head, and knows not that it brings abundance to drive away the hunger",
        "A rainy day is the perfect time for a walk in the woods",
        "There's always a period of curious fear between the first sweet-smelling breeze and the time when the rain comes cracking down",
    ])

cloudy = WeatherType(

    bbc_phrases={"partial cloud": 1, "white cloud": 1, "grey cloud": 1},
    rx="cloud",
    emoji=[
        emojihelper.sun_behind_cloud,
        emojihelper.cloud
    ],
    phrases=[
        "I'm on cloud nine",
        "Every cloud has a silver lining",
        "Behind every cloud is another cloud",
        "There's a bright spot in every dark cloud",
        "I'm somewhat in my own cloud",
        "Every silver lining has a cloud",
        "is this cloud computing?",

        "The cloud never comes from the quarter of the horizon from which we watch for it",
        "Above the cloud with its shadow is the star with its light. Above all things reverence thyself",
        "Every cloud has its silver lining but it is sometimes a little difficult to get it to the mint",
        "Happiness is like a cloud, if you stare at it long enough, it evaporates",
        "Clouds come floating into my life, no longer to carry rain or usher storm, but to add color to my sunset sky",
        "Who cares about the clouds when we're together? Just sing a song and bring the sunny weather",
        "A cloudy day is no match for a sunny disposition",
        "Clouds come floating into my life, no longer to carry rain or usher storm, but to add color to my sunset sky",

    ])

windy = WeatherType(
    bbc_phrases={"a little wind": 1, "a strong breeze": 2},
    rx="wind|windy|breeze|breezy|blustery|gusts",
    emoji=[
        emojihelper.wind_blowing_face,
        emojihelper.wind_chime,
        emojihelper.leaf_fluttering_in_wind,
    ], phrases=[
        "I'll get my kite",

        "When the wind is out of the East, tis never good for man nor beast",
        "If crows fly low, winds going to blow; If crows fly high, winds going to die",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination",
        "The fragrance of flowers spreads only in the direction of the wind. But the goodness of a person spreads in all directions",
        "Thought is the wind, knowledge the sail, and mankind the vessel",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it",
        "If you are bitter, you are like a dry leaf that you can just squash, and you can get blown away by the wind. There is much more wisdom in forgiveness",
        "Notice that the stiffest tree is most easily cracked, while the bamboo or willow survives by bending with the wind",
        "If one does not know to which port one is sailing, no wind is favorable",
        "The pessimist complains about the wind; the optimist expects it to change; the realist adjusts the sails",
        "You must take personal responsibility. You cannot change the circumstances, the seasons, or the wind, but you can change yourself. That is something you have charge of",
        "No one but night, with tears on her dark face, watches beside me in this windy place",
    ])

weather_types = [
    snow,
    storm,
    freeze,
    hot,
    warm,
    sunny,
    rainy,
    cold,
    cloudy,
    windy

]

generic_weather_responses = [
    "Whether it's cold or whether it's hot; We shall have weather, whether or not!",
    "No weather is ill, if the wind is still",
    "Red sky at night, shepherd's delight. Red sky in the morning, shepherd's warning",
    "Mackerel sky and mare's tails make tall ships carry low sails",
    "Sunshine is delicious, rain is refreshing, wind braces us up, snow is exhilarating; there is really no such thing as bad weather, only different kinds of good weather",
    "Wherever you go, no matter what the weather, always bring your own sunshine",
    "The trouble with weather forecasting is that it's right too often for us to ignore it and wrong too often for us to rely on it",
    "Weather is a great metaphor for life — sometimes it's good, sometimes it's bad, and there's nothing much you can do about it but carry an umbrella or choose to dance in the rain",
    "To be interested in the changing seasons is a happier state of mind than to be hopelessly in love with spring",
    "Don't knock the weather; nine-tenths of the people couldn't start a conversation if it didn't change once in a while",
    "There’s no such thing as bad weather, only unsuitable clothing",
    "On cable TV they have a weather channel — 24 hours of weather. We had something like that where I grew up. We called it a window",
]

high = [5, 6, 7, 10, 13, 16, 18, 18, 15, 11, 7, 5]
avg = [3, 4, 5, 7, 10, 12, 14, 15, 12, 9, 5, 3]
low = [1, 1, 2, 3, 6, 8, 10, 11, 9, 6, 3, 1]

average_high_low_temperatures = list(zip(low, avg, high))


def get_weather_response(text):
    for weather_type in weather_types:
        if weather_type.is_match(text):
            return weather_type.get_phrase()

    return phrase_generator.generate_phrase(generic_weather_responses)


def is_weather(text):
    for weather_type in weather_types:
        if weather_type.is_match(text):
            return weather_type
