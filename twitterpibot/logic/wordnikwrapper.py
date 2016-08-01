import logging
import random

# noinspection PyPackageRequirements
from wordnik import swagger, WordApi, WordsApi, WordListApi, WordListsApi, AccountApi
from twitterpibot.data_access import dal

logger = logging.getLogger(__name__)

_init = False

word_api = None
words_api = None
word_list_api = None
word_lists_api = None

account_api = None
auth_token = None


def init():
    global _init

    global word_api
    global words_api
    global word_list_api
    global word_lists_api

    global account_api
    global auth_token

    if not _init:
        apiUrl = 'http://api.wordnik.com/v4'
        apiKey = dal.get_token("wordnik api")
        client = swagger.ApiClient(apiKey, apiUrl)

        account_api = AccountApi.AccountApi(client)
        username = dal.get_token("wordnik username")
        password = dal.get_token("wordnik password")
        auth_token = account_api.authenticate(username, password).token

        word_api = WordApi.WordApi(client)
        words_api = WordsApi.WordsApi(client)
        word_list_api = WordListApi.WordListApi(client)
        word_lists_api = WordListsApi.WordListsApi(client)

        _init = True


def get_words_matching(stem):
    init()

    skip = 0
    limit = 1000

    search = words_api.searchWords("*%s*" % stem, skip=skip, limit=limit)
    words = list(map(lambda w: w.word, search.searchResults))
    logger.debug(words)

    return words


def get_word_matching(stem, rx):
    init()
    words = []
    word = None
    skip = 0
    limit = 1000
    while not word or (rx and not rx.match(word)):
        if not words:
            search = words_api.searchWords("*%s*" % stem, skip=skip, limit=limit)
            words = list(map(lambda w: w.word, search.searchResults))
            random.shuffle(words)
            skip += 1 * limit

            logger.debug(words)
        word = words.pop()

    return word


def get_example(word):
    init()
    examples = word_api.getExamples(word)
    example = random.choice(examples.examples)
    return example.text
