import os
try: input = raw_input
except NameError: pass

import pickle
from twython.api import Twython

def GetTokens(screen_name):

    app_key_path = "APP_KEY.pkl"
    app_secret_path = "APP_SECRET.pkl"
    final_oauth_token_path = screen_name + "_FINAL_OAUTH_TOKEN.pkl"
    final_oauth_token_secret_path = screen_name + "FINAL_OAUTH_TOKEN_SECRET.pkl"

    exists = os.path.isfile(app_key_path) and os.path.isfile(app_secret_path)

    if (exists):
        APP_KEY = pickle.load(open(app_key_path, "rb"))
        APP_SECRET = pickle.load(open(app_secret_path, "rb"))
    else:
        APP_KEY = input("Enter your APP_KEY:")
        APP_SECRET = input("Enter your APP_SECRET:")
        
        pickle.dump(APP_KEY, open(app_key_path, "wb"))
        pickle.dump(APP_SECRET, open(app_secret_path, "wb"))

    exists = os.path.isfile(final_oauth_token_path) and os.path.isfile(final_oauth_token_secret_path)

    if (exists):

        FINAL_OAUTH_TOKEN = pickle.load(open(final_oauth_token_path, "rb"))
        FINAL_OAUTH_TOKEN_SECRET = pickle.load(open(final_oauth_token_secret_path, "rb"))

    else:

        twitter = Twython(APP_KEY, APP_SECRET)

        auth = twitter.get_authentication_tokens()

        OAUTH_TOKEN = auth["oauth_token"]
        OAUTH_TOKEN_SECRET = auth["oauth_token_secret"]

        url = auth["auth_url"]
        print(url)
        webbrowser.open(url)

        oauth_verifier = input("Enter your pin:")

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        final_step = twitter.get_authorized_tokens(oauth_verifier)

        FINAL_OAUTH_TOKEN = final_step["oauth_token"]
        FINAL_OAUTH_TOKEN_SECRET = final_step["oauth_token_secret"]

        pickle.dump(FINAL_OAUTH_TOKEN, open(final_oauth_token_path, "wb"))
        pickle.dump(FINAL_OAUTH_TOKEN_SECRET, open(final_oauth_token_secret_path, "wb"))

    tokens = [APP_KEY, APP_SECRET, FINAL_OAUTH_TOKEN, FINAL_OAUTH_TOKEN_SECRET]
   
    return tokens