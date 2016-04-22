from twitterpibot.logic.cypher_helper import SubstitutionCypher


class LeetSpeak(SubstitutionCypher):
    def __init__(self):
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
        super(LeetSpeak, self).__init__(_encode, _decode)


if __name__ == '__main__':
    cypher = LeetSpeak()
    print(cypher.encode("ALL YOUR BASE ARE BELONG TO US"))
