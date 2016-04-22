from collections import Counter
import logging
import pprint
import random
import re
import statistics
import string
import math
from twitterpibot.logic import english
from twitterpibot.logic.cypher_helper import SubstitutionCypher, logger

__author__ = 'andrewtatham'

logger = logging.getLogger(__name__)


class RandomCypher(SubstitutionCypher):
    def __init__(self):
        # symbols = list(set(string.ascii_uppercase).union(set(string.digits)))
        symbols = list(string.ascii_uppercase)
        list1 = list(symbols)
        list2 = list(symbols)
        random.shuffle(list1)
        random.shuffle(list2)
        encode_pairs = zip(list1, list2)
        decode_pairs = zip(list2, list1)
        encode = dict(encode_pairs)
        decode = dict(decode_pairs)
        logger.debug(encode)
        logger.debug(decode)
        super(RandomCypher, self).__init__(encode, decode)

    def guess(self, encode_guess, decode_guess):

        return statistics.mean([
            self.score(self._encode, encode_guess),
            self.score(self._decode, decode_guess)
        ])

    def score(self, mapping, mapping_guess):
        total = len(mapping)
        score = 0
        for k, v in mapping.items():
            if k in mapping_guess and mapping_guess[k] == v:
                score += 1

        return score / total


class Code(object):
    def __init__(self, code, cheat_text=None):
        self.code = code
        self.words = code.split(" ")
        self.word_starts = [m.start() for m in re.finditer('[\w]+', code)]
        self.lengths = list(map(lambda word: len(word), self.words))
        self.lengths_string = " ".join(map(lambda length: str(length), self.lengths))
        self.cheat_text = cheat_text

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def _find_pattern_by_length(self, pattern):
        if pattern.lengths_string in self.lengths_string:

            # will only find first match
            offset = self.lengths.index(pattern.lengths[0])
            if all(map(lambda i: self.lengths[offset + i] == pattern.lengths[i], range(len(pattern.words)))):
                return Pattern(" ".join(map(lambda i: self.words[offset + i], range(len(pattern.words)))))
        return None


class Pattern(Code):
    def __init__(self, code):
        super(Pattern, self).__init__(code)

        symbol_id = 65
        self.symbol_map = {" ": " "}
        for letter in code:
            if letter not in self.symbol_map:
                self.symbol_map[letter] = chr(symbol_id)
                symbol_id += 1
        self.pattern = ""
        for letter in code:
            self.pattern += str(self.symbol_map[letter])

    def get_reverse_map(self):
        return dict([(v, k) for k, v in self.symbol_map.items()])


class Codes(object):
    def __init__(self):
        self._codes = []

    def add_code(self, code, cheat_text=None):
        self._codes.append(Code(code, cheat_text))

    def get_all_text(self):
        all_text = " ".join(map(lambda code: code.code, self._codes))
        return all_text

    def get_all_words(self):
        all_words = []
        for code in self._codes:
            all_words.extend(code.words)
        return all_words

    def find_pattern(self, pattern):
        for code in self._codes:
            match = code._find_pattern_by_length(pattern)
            if match:
                if self.match_symbols(match, pattern):
                    code_symbols = match.get_reverse_map()
                    text_symbols = pattern.get_reverse_map()

                    encode = {}
                    decode = {}

                    for symbol_id in code_symbols:
                        code_letter = code_symbols[symbol_id]
                        text_letter = text_symbols[symbol_id]

                        encode[text_letter] = code_letter
                        decode[code_letter] = text_letter

                    return encode, decode
        return None, None

    def match_symbols(self, match, pattern):
        return match.pattern == pattern.pattern


class RandomCypherBreaker(object):
    def __init__(self, expected_phrases=None):
        self.english_letter_frequency = list("ETAOINSHRDLCUMWFGYPBVKJXQZ")
        self._codes = Codes()
        self._encode = {}
        self._decode = {}
        self.expected_phrases = expected_phrases

    def add_code(self, code, cheat_text=None):
        self._codes.add_code(code, cheat_text)

    def analyse_letter_frequency(self):
        return Counter(self._codes.get_all_text()).most_common()

    def analyse_word_frequency(self):
        return Counter(self._codes.get_all_words()).most_common()

    def pattern_match(self, expected_phrase):

        pattern = Pattern(expected_phrase)
        if pattern:
            encode, decode = self._codes.find_pattern(pattern)
            if encode:
                self._encode.update(encode)
            if decode:
                self._decode.update(decode)

    def get_guess(self):
        if self.expected_phrases:

            for expected_phrase in self.expected_phrases:
                self.pattern_match(expected_phrase)

        expected_plurals = {
            "HUMAN": "HUMANS",
            "MAMMAL": "MAMMALS",
            "MACHINE": "MACHINES"
        }
        estimated_score = 0
        if self._encode and self._decode:
            candidate = SubstitutionCypher(self._encode, self._decode)
            total_score = 0
            n = len(self._codes._codes)
            for code in self._codes._codes:
                decoded = candidate.decode(code.code)
                # logger.info(decoded)
                # score based on common english words
                words = english.get_common_words(decoded)

                score = len(words["common"]) / (len(words["uncommon"]) + len(words["common"]))
                total_score += score

            estimated_score = total_score / n
        return {
            "estimated_score": estimated_score,
            "encode": self._encode,
            "decode": self._decode
        }


if __name__ == '__main__':
    from twitterpibot.logic import judgement_day

    logging.basicConfig(level=logging.INFO)
    expected_phrases = []
    for _ in range(3):
        expected_phrases.append(judgement_day.phrase())

    cypher = RandomCypher()
    breaker = RandomCypherBreaker(expected_phrases=expected_phrases)

    # news_headlines = feedhelper.get_news_stories()
    for _ in range(100):
        text = judgement_day.phrase()

        text = text.upper()
        logger.info("Text: " + text)
        code = cypher.encode(text)
        logger.info("Code: " + code)

        breaker.add_code(code, text)

        guess = breaker.get_guess()
        guess_cypher = SubstitutionCypher(guess["encode"], guess["decode"])
        decoded_text = guess_cypher.decode(code)

        score = 0
        n = len(text)
        for i in range(n):
            if text[i] == decoded_text[i]:
                score += 1
        score /= n

        logger.info("Decoded: " + decoded_text)

        logger.info("Estimated Score: {}".format(guess["estimated_score"]))
        logger.info("Actual Score: {}".format(score))

        cypher_score = cypher.guess(guess["encode"], guess["decode"])
        logger.info("Actual cypher_score: " + pprint.pformat(cypher_score))
