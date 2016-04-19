from twitterpibot.logic import judgement_day, morse_code
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


if __name__ == '__main__':
    p = judgement_day.phrase()
    print(p)
    l = encode(p)
    print(l)
    m = morse_code.encode(l)

    print(len(m),m)
    l = morse_code.decode(m)
    print(l)
    print(decode(l))
