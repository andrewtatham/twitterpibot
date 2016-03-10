import os
import webbrowser
import sys

from twitterpibot.logic import fsh

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

    tokens_dir = fsh.root + "temp" + os.sep + "tokens" + os.sep + str(sys.version_info[0]) + os.sep
    fsh.ensure_directory_exists(tokens_dir)

    csv_path=tokens_dir+"tokens.csv"
    tokens_csv = None
    if fsh.exists(csv_path):
        tokens_csv = fsh.parse_csv(csv_path)

    app_key_path = tokens_dir + screen_name + "_APP_KEY.pkl"
    app_secret_path = tokens_dir + screen_name + "_APP_SECRET.pkl"
    final_oauth_token_path = tokens_dir + screen_name + "_FINAL_OAUTH_TOKEN.pkl"
    final_oauth_token_secret_path = tokens_dir + screen_name + "_FINAL_OAUTH_TOKEN_SECRET.pkl"

    exists = os.path.isfile(app_key_path) and os.path.isfile(app_secret_path)
    if exists:
        app_key = pickle.load(open(app_key_path, "rb"))
        app_secret = pickle.load(open(app_secret_path, "rb"))
    else:
        if tokens_csv and screen_name in tokens_csv:
            app_key = tokens_csv[screen_name][1]
            app_secret = tokens_csv[screen_name][2]
        else:
            input("Please ensure you are logged in as " + screen_name + " and press enter")
            app_key = input("Enter your APP_KEY:")
            app_secret = input("Enter your APP_SECRET:")

        pickle.dump(app_key, open(app_key_path, "wb"))
        pickle.dump(app_secret, open(app_secret_path, "wb"))

    exists = os.path.isfile(final_oauth_token_path) and os.path.isfile(final_oauth_token_secret_path)

    if exists:

        final_oauth_token = pickle.load(open(final_oauth_token_path, "rb"))
        final_oauth_token_secret = pickle.load(open(final_oauth_token_secret_path, "rb"))

    else:

        twitter = Twython(app_key, app_secret)

        auth = twitter.get_authentication_tokens()

        oauth_token = auth["oauth_token"]
        oauth_token_secret = auth["oauth_token_secret"]

        input("Please ensure you are logged in as " + screen_name + " and press enter")
        url = auth["auth_url"]
        logger.info(url)
        webbrowser.open(url)

        oauth_verifier = input("Please enter your pin:")

        twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

        final_step = twitter.get_authorized_tokens(oauth_verifier)

        final_oauth_token = final_step["oauth_token"]
        final_oauth_token_secret = final_step["oauth_token_secret"]

        pickle.dump(final_oauth_token, open(final_oauth_token_path, "wb"))
        pickle.dump(final_oauth_token_secret, open(final_oauth_token_secret_path, "wb"))

    tokens = [app_key, app_secret, final_oauth_token, final_oauth_token_secret]

    return tokens
