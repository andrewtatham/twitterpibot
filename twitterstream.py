




from twython import Twython, TwythonStreamer

import time
from datetime import datetime
import os.path
from os import listdir
import pickle
import pprint


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            # STATUS UPDATE

            tweetstring = data['id_str'].encode('utf-8') + ': ' + data['user']['name'].encode('utf-8') + ' [@' + data['user']['screen_name'].encode('utf-8') + '] "' + data['text'].encode('utf-8') + '"'
            print(tweetstring)

            #print(data['text'].encode('utf-8'))    
            #pprint.pprint(data)
        elif 'direct_message' in data:
            # DIRECT MESSAGE
            senderid = str(data['direct_message']['sender_id_str'])
            sender = str(data['direct_message']['sender_screen_name'])
            
            print("Direct message from " + sender + ' ' + senderid )
            
            if senderid == andrewpiid:
                # IGNORE
                pass
                print(" from pi" )
            elif senderid == andrewid:
                # FROM ME
                print(" from me" )
            else:
                pprint.pprint(data)
            

            
        else:
            #pass
            pprint.pprint(data)

            
    def on_error(self, status_code, data):

            print(str(status_code)  + ' ' + data)





def Authenticate():
    # APP_KEY = 'xglqZ20zTPe97yq0ZLkQsV2af'
    # APP_SECRET = 'ci0fovVfpRrxuqP9C0KwAxl1tajH8yJoxQcSuUNYluFBxpS9Au'
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

    
   
    streamer = MyStreamer(APP_KEY, APP_SECRET, FINAL_OAUTH_TOKEN, FINAL_OAUTH_TOKEN_SECRET)

    return streamer




    
    



andrewpi = "@andrewtathampi" 
andrewpiid = "2935295111"

andrew = "@andrewtatham"
andrewid = "19201332"

helen = "@morris_helen"
markr = "@fuuuunnnkkytree"
jamie = "@jami3rez"
dean = "@dcspamoni"
chriswatson = "@watdoghotdog"
fletch = "@paulfletcher79"
simon = "@Tolle_Lege"

users = [andrew, markr, jamie, helen, dean, chriswatson, simon]






streamer = Authenticate()


#userids = users
#userscsv = ','.join(userids)
#print(userscsv)
#myfilter = "andrewtatham" # userscsv

## streamer.statuses.sample()

## streamer.statuses.filter(track='Leeds',language='en',stall_warnings='true', filter_level='medium')

## streamer.user()

streamer.user()


####streamer.statuses.firehose()


    
