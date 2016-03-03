import logging

from wordnik import swagger, WordApi, WordsApi, WordListApi, WordListsApi, AccountApi

import twitterpibot.logic.FileSystemHelper as fsh

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

my_lists = account_api.getWordListsForLoggedInUser(auth_token)
for my_list in my_lists:
    print("{username}, {name}, {numberWordsInList}, {description}, {permalink}".format(**my_list.__dict__))
    list_words = word_list_api.getWordListWords(permalink=my_list.permalink, auth_token=auth_token)
    for word in list_words:
        print(word.word)

random_words = words_api.getRandomWords()
for word in random_words:
    print(word.word)
    definitions = word_api.getDefinitions(word.word)
    print(" definitons:")
    for definition in definitions:
        print("  " + definition.text)
