import pprint
import logging

from wordnik import swagger, WordApi, WordsApi

import twitterpibot.logic.FileSystemHelper as fsh

logger = logging.getLogger(__name__)

apiUrl = 'http://api.wordnik.com/v4'
apiKey = fsh.get_key('wordnik')
client = swagger.ApiClient(apiKey, apiUrl)

word_api = WordApi.WordApi(client)
words_api = WordsApi.WordsApi(client)

random_words = words_api.getRandomWords()
for word in random_words:
    print(word.word)
    definitions = word_api.getDefinitions(word.word)
    print(" definitons:")
    for definition in definitions:
        print("  " + definition.text)

