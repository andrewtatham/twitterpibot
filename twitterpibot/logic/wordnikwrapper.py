import logging

from wordnik import swagger, WordApi, WordsApi, WordListApi, WordListsApi

import twitterpibot.logic.FileSystemHelper as fsh

logger = logging.getLogger(__name__)

apiUrl = 'http://api.wordnik.com/v4'
apiKey = fsh.get_key('wordnik')
client = swagger.ApiClient(apiKey, apiUrl)

word_api = WordApi.WordApi(client)
words_api = WordsApi.WordsApi(client)
word_list_api = WordListApi.WordListApi(client)
word_lists_api = WordListsApi.WordListsApi(client)

lists = [
    "https://www.wordnik.com/lists/words-i-wish-i-didnt-know",
    "https://www.wordnik.com/lists/aftercrimes--geoslavery--and-thermogeddon",
    "https://www.wordnik.com/lists/outcasts",
    "https://www.wordnik.com/lists/twitter-favourites",
    "https://www.wordnik.com/lists/twitter-favorites",
    "https://www.wordnik.com/lists/twitter-loves",
    "https://www.wordnik.com/lists/twitter-hates"]
word_list_api.getWordListByPermalink("https://www.wordnik.com/lists/twitter-loves")


def get_random_words():
    random_words = words_api.getRandomWords()
    for word in random_words:
        print(word.word)
        definitions = word_api.getDefinitions(word.word)
        print(" definitons:")
        for definition in definitions:
            print("  " + definition.text)
