from itertools import cycle
import string
import logging

logger = logging.getLogger(__name__)


def _map(mapping, letter_in):
    logger.debug("letter in: {}".format(letter_in))
    if letter_in in mapping:

        letter_out = mapping[letter_in]
    else:
        letter_out = letter_in
    logger.debug("letter out: {}".format(letter_out))
    return letter_out


class SubstitutionCypher(object):
    def __init__(self, encode, decode,
                 encode_in_word_sep=" ", encode_in_sep="", encode_out_sep="", encode_out_word_sep=" ",
                 decode_in_word_sep=" ", decode_in_sep="", decode_out_sep="", decode_out_word_sep=" "

                 ):
        self._encode = encode
        self._decode = decode

        self._encode_in_word_sep = encode_in_word_sep
        self._encode_in_sep = encode_in_sep
        self._encode_out_sep = encode_out_sep
        self._encode_out_word_sep = encode_out_word_sep

        self._decode_in_word_sep = decode_in_word_sep
        self._decode_in_sep = decode_in_sep
        self._decode_out_sep = decode_out_sep
        self._decode_out_word_sep = decode_out_word_sep

    def encode(self, text):
        logger.debug("encode text: {}".format(text))
        if self._encode_in_word_sep:
            words = text.split(self._encode_in_word_sep)
        else:
            words = text
        logger.debug("encode words: {}".format(words))

        if self._encode_in_sep:
            letters = list(map(lambda word: word.split(self._encode_in_sep), words))
        else:
            letters = list(map(lambda word: list(word), words))
        logger.debug("encode letters: {}".format(letters))

        code_words = list(map(self._encode_word, letters))

        logger.debug("encode code_words: {}".format(code_words))
        code = self._encode_out_word_sep.join(code_words)
        logger.debug("encode code: {}".format(code))
        return code

    def decode(self, code):
        logger.debug("decode code: {}".format(code))
        if self._decode_in_word_sep:
            code_words = code.split(self._decode_in_word_sep)
        else:
            code_words = code
        logger.debug("decode code_words: {}".format(code_words))

        if self._decode_in_sep:
            code_letters = list(map(lambda code_word: code_word.split(self._decode_in_sep), code_words))
        else:
            code_letters = list(map(lambda code_word: list(code_word), code_words))
        logger.debug("decode code_letters: {}".format(code_letters))

        words = list(map(self._decode_word, code_letters))

        logger.debug("decode words: {}".format(words))
        text = self._decode_out_word_sep.join(words)
        logger.debug("decode text: {}".format(text))
        return text

    def _decode_word(self, word):
        return self._decode_out_sep.join(list(map(self._decode_letter, word)))

    def _decode_letter(self, letter):
        return _map(self._decode, letter)

    def _encode_letter(self, letter):
        return _map(self._encode, letter)

    def _encode_word(self, code_word):
        return self._encode_out_sep.join(list(map(self._encode_letter, code_word)))


class SimpleCypher(SubstitutionCypher):
    def __init__(self):
        letters = list(string.ascii_uppercase)
        letters_reversed = list(letters)
        letters_reversed.reverse()

        numbers = list(string.digits)
        numbers_reversed = list(numbers)
        numbers_reversed.reverse()

        encode_decode = dict(zip(letters, letters_reversed))
        encode_decode.update(dict(zip(numbers, numbers_reversed)))
        super(SimpleCypher, self).__init__(encode_decode, encode_decode)


class CeaserCypher(SubstitutionCypher):
    def __init__(self, shift):

        encode = {}
        decode = {}
        symbols = list(string.ascii_uppercase + string.digits)
        symbols_shifted = cycle(symbols)
        for _ in range(abs(shift)):
            next(symbols_shifted)
        for symbol in symbols:
            symbol_shifted = next(symbols_shifted)
            if shift >= 0:
                encode[symbol] = symbol_shifted
                decode[symbol_shifted] = symbol
            else:
                decode[symbol] = symbol_shifted
                encode[symbol_shifted] = symbol

        super(CeaserCypher, self).__init__(encode, decode)
