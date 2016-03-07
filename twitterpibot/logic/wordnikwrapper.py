import logging
import random

# noinspection PyPackageRequirements
from wordnik import swagger, WordApi, WordsApi, WordListApi, WordListsApi, AccountApi

import twitterpibot.logic.fsh as fsh

logger = logging.getLogger(__name__)

key_name = "wordnik"

apiUrl = 'http://api.wordnik.com/v4'
apiKey = fsh.get_key(key_name)
client = swagger.ApiClient(apiKey, apiUrl)

account_api = AccountApi.AccountApi(client)
username = fsh.get_username(key_name)
password = fsh.get_password(key_name)
auth_token = account_api.authenticate(username, password).token

word_api = WordApi.WordApi(client)
words_api = WordsApi.WordsApi(client)
word_list_api = WordListApi.WordListApi(client)
word_lists_api = WordListsApi.WordListsApi(client)


def _get_egg_puns_list():
    words = []
    list_words = word_list_api.getWordListWords(permalink="egg-puns", auth_token=auth_token, limit=10000)
    if list_words:
        for word in list_words:
            words.append(word.word)
    return words


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def _build_egg_puns_list():
    generated = set(_generate_egg_puns())
    existing = set(_get_egg_puns_list())
    new_puns = list(generated.difference(existing))

    if new_puns:
        for chunk in chunks(new_puns, 100):
            print("adding " + chunk[0] + " to " + chunk[-1])
            word_list_api.addWordsToWordList(permalink="egg-puns", auth_token=auth_token, body=chunk)


def _generate_egg_puns():
    puns = []

    for repl in [("ig", "egg"), ("ex", "eggs")]:
        for i in range(100):
            search = words_api.searchWords("*" + repl[0] + "*", skip=i * 1000, limit=10000)
            for w in search.searchResults:
                if repl[0] in w.word:
                    pun = w.word.replace(repl[0], repl[1])
                    puns.append(pun)
                    # print(egg_word.word + " => " + pun)
    return puns


def get_lists():
    my_lists = account_api.getWordListsForLoggedInUser(auth_token)
    for my_list in my_lists:
        print("{username}, {name}, {numberWordsInList}, {description}, {permalink}".format(**my_list.__dict__))
        list_words = word_list_api.getWordListWords(permalink=my_list.permalink, auth_token=auth_token, limit=10000)
        if list_words:
            for word in list_words:
                print(" " + word.word)


def get_random_words():
    random_words = words_api.getRandomWords()
    for word in random_words:
        print(word.word)
        definitions = word_api.getDefinitions(word.word)
        print(" definitons:")
        for definition in definitions:
            print("  " + definition.text)


if __name__ == "__main__":
    get_lists()
    _build_egg_puns_list()

egg_puns = _get_egg_puns_list()


# print(egg_puns)


def get_egg_puns():
    return egg_puns


def get_word_matching(stem, rx):
    words = []
    word = None
    skip = 0
    limit = 1000
    while not word or not rx.match(word):
        if not words:
            search = words_api.searchWords("*%s*" % stem, skip=skip, limit=limit)
            words = list(map(lambda w: w.word, search.searchResults))
            random.shuffle(words)
            skip += 1 * limit

            logger.debug(words)
        word = words.pop()

    return word


def get_example(word):
    examples = word_api.getExamples(word)
    example = random.choice(examples.examples)
    return example.text
