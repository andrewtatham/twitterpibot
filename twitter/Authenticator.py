import os
import pickle
class Authenticator(object):

    def Authenticate(args):
    
        exists = os.path.isfile("APP_KEY.pkl") and os.path.isfile("APP_SECRET.pkl")

        if (exists):
            APP_KEY = pickle.load(open("APP_KEY.pkl", "rb"))
            APP_SECRET = pickle.load(open("APP_SECRET.pkl", "rb"))
        else:
            APP_KEY = raw_input("Enter your APP_KEY:")
            APP_SECRET = raw_input("Enter your APP_SECRET:")
        
            pickle.dump(APP_KEY, open("APP_KEY.pkl", "wb"))
            pickle.dump(APP_SECRET, open("APP_SECRET.pkl", "wb"))

        exists = os.path.isfile("FINAL_OAUTH_TOKEN.pkl") and os.path.isfile("FINAL_OAUTH_TOKEN_SECRET.pkl")

        if (exists):

            FINAL_OAUTH_TOKEN = pickle.load(open("FINAL_OAUTH_TOKEN.pkl", "rb"))
            FINAL_OAUTH_TOKEN_SECRET = pickle.load(open("FINAL_OAUTH_TOKEN_SECRET.pkl", "rb"))

        else:

            twitter = Twython(APP_KEY, APP_SECRET)

            auth = twitter.get_authentication_tokens()

            OAUTH_TOKEN = auth["oauth_token"]
            OAUTH_TOKEN_SECRET = auth["oauth_token_secret"]

            print(auth["auth_url"])

            oauth_verifier = raw_input("Enter your pin:")

            twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

            final_step = twitter.get_authorized_tokens(oauth_verifier)

            FINAL_OAUTH_TOKEN = final_step["oauth_token"]
            FINAL_OAUTH_TOKEN_SECRET = final_step["oauth_token_secret"]

            pickle.dump(FINAL_OAUTH_TOKEN, open("FINAL_OAUTH_TOKEN.pkl", "wb"))
            pickle.dump(FINAL_OAUTH_TOKEN_SECRET, open("FINAL_OAUTH_TOKEN_SECRET.pkl", "wb"))

        tokens = [APP_KEY, APP_SECRET, FINAL_OAUTH_TOKEN, FINAL_OAUTH_TOKEN_SECRET]
   
        return tokens
