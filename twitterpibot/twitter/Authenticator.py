import os
import webbrowser

try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    input = raw_input
except NameError:
    pass

import pickle
from twython.api import Twython
import logging

logger = logging.getLogger(__name__)


def get_tokens(screen_name):
    dir = "temp" + os.sep + "tokens" + os.sep

    if not os.path.exists(dir):
        os.makedirs(dir)

    app_key_path = dir + "APP_KEY.pkl"
    app_secret_path = dir + "APP_SECRET.pkl"
    final_oauth_token_path = dir + screen_name + "_FINAL_OAUTH_TOKEN.pkl"
    final_oauth_token_secret_path = dir + screen_name + "_FINAL_OAUTH_TOKEN_SECRET.pkl"

    exists = os.path.isfile(app_key_path) and os.path.isfile(app_secret_path)

    if exists:
        APP_KEY = pickle.load(open(app_key_path, "rb"))
        APP_SECRET = pickle.load(open(app_secret_path, "rb"))
    else:
        APP_KEY = input("Enter your APP_KEY:")
        APP_SECRET = input("Enter your APP_SECRET:")

        pickle.dump(APP_KEY, open(app_key_path, "wb"))
        pickle.dump(APP_SECRET, open(app_secret_path, "wb"))

    exists = os.path.isfile(final_oauth_token_path) and os.path.isfile(final_oauth_token_secret_path)

    if exists:

        final_oauth_token = pickle.load(open(final_oauth_token_path, "rb"))
        final_oauth_token_secret = pickle.load(open(final_oauth_token_secret_path, "rb"))

    else:

        twitter = Twython(APP_KEY, APP_SECRET)

        auth = twitter.get_authentication_tokens()

        oauth_token = auth["oauth_token"]
        oauth_token_secret = auth["oauth_token_secret"]

        url = auth["auth_url"]
        logger.info(url)
        webbrowser.open(url)

        oauth_verifier = input("Enter your pin:")

        twitter = Twython(APP_KEY, APP_SECRET, oauth_token, oauth_token_secret)

        final_step = twitter.get_authorized_tokens(oauth_verifier)

        final_oauth_token = final_step["oauth_token"]
        final_oauth_token_secret = final_step["oauth_token_secret"]

        pickle.dump(final_oauth_token, open(final_oauth_token_path, "wb"))
        pickle.dump(final_oauth_token_secret, open(final_oauth_token_secret_path, "wb"))

    tokens = [APP_KEY, APP_SECRET, final_oauth_token, final_oauth_token_secret]

    return tokens
