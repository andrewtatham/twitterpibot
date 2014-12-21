


# APP_KEY = 'xglqZ20zTPe97yq0ZLkQsV2af'
# APP_SECRET = 'ci0fovVfpRrxuqP9C0KwAxl1tajH8yJoxQcSuUNYluFBxpS9Au'

from twython import Twython
import time
from datetime import datetime
import os.path
import pickle

def Authenticate():
    APP_KEY = 'xglqZ20zTPe97yq0ZLkQsV2af'
    APP_SECRET = 'ci0fovVfpRrxuqP9C0KwAxl1tajH8yJoxQcSuUNYluFBxpS9Au'

    exists = os.path.isfile('FINAL_OAUTH_TOKEN.pkl') and os.path.isfile('FINAL_OAUTH_TOKEN_SECRET.pkl')

    if (exists):

        FINAL_OAUTH_TOKEN = pickle.load(open("FINAL_OAUTH_TOKEN.pkl", "rb"))
        FINAL_OAUTH_TOKEN_SECRET = pickle.load(open("FINAL_OAUTH_TOKEN_SECRET.pkl", "rb"))

    else:

        twitter = Twython(APP_KEY, APP_SECRET)

        auth = twitter.get_authentication_tokens()

        OAUTH_TOKEN = auth['oauth_token']
        OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

        print(auth['auth_url'])

        oauth_verifier = raw_input('Enter your pin:')

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        final_step = twitter.get_authorized_tokens(oauth_verifier)

        FINAL_OAUTH_TOKEN = final_step['oauth_token']
        FINAL_OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

        pickle.dump(FINAL_OAUTH_TOKEN, open("FINAL_OAUTH_TOKEN.pkl", "wb"))
        pickle.dump(FINAL_OAUTH_TOKEN_SECRET, open("FINAL_OAUTH_TOKEN_SECRET.pkl", "wb"))
   
    twitter = Twython(APP_KEY, APP_SECRET, FINAL_OAUTH_TOKEN, FINAL_OAUTH_TOKEN_SECRET)

    return twitter

    

twitter = Authenticate()

andrew = "@andrewtatham"
helen = "@morris_helen"
markr = "@fuuuunnnkkytree"
jamie = "@jami3rez"
dean = "@dcspamoni"
chriswatson = "@watdoghotdog"
fletch = "@paulfletcher79"
simon = "@Tolle_Lege"


while (True):
    timeline = twitter.get_home_timeline()
    for tweet in timeline:
        print(tweet['text'])

    status = "@morris_helen it is " + str(datetime.now())
    twitter.update_status(status=status)
    time.sleep(60)
    
