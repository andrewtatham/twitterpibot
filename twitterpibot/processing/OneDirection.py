import re

_one_direction = [
    "1D",
    "One Direction",
    "Niall", "Horan",
    "Liam", "Payne",
    "Harry", "Styles",
    "Louis", "Tomlinson",
    "Zayn", "Malik"

]

_five_seconds_of_summer = [
    "5SOS",
    "five seconds of summer",
    "Luke", "Hemmings",
    "Michael", "Clifford",
    "Calum", "Hood",
    "Ashton", "Irwin"
]

_kardashians = [
    "Kardashian",
    "Kim",
    "Khloe",
    "Kourtney",
    "Kylie",
    "Kendall",
    "Caitlyn",
    "Jenner"
]

_other = [
    "Justin Bieber",
    "Miley Cyrus",
    "Taylor Swift",
    "Britney Spears",
    "Ariana Grande"
]

_one_direction_rx = re.compile("|".join(_one_direction), re.IGNORECASE)


def is_one_direction(text):
    matches = _one_direction_rx.findall(text)
    return bool(matches)
