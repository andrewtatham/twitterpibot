from twitterpibot.logic.cypher_helper import _map

subs = [
    ("I", "1"),
    ("O", "0"),
    ("S", "5"),
    ("Z", "2"),
    ("E", "3"),
    ("A", "4"),
    ("T", "7"),
    ("B", "8"),

]

_encode = dict([(k, v) for k, v in subs])
_decode = dict([(v, k) for k, v in subs])


def encode(text):
    code = "".join(map(lambda letter: _map(_encode, letter), list(text)))
    return code


def decode(code):
    code = "".join(map(lambda letter: _map(_decode, letter), list(code)))
    return code
