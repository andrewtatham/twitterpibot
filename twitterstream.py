

# features/fixes

# smaller image size to prevet hangs
# case insensitivity
# mentions/retweets



from twython import Twython, TwythonStreamer

import time
from datetime import datetime
import pickle
import pprint
import random

from os import listdir
import os.path


import picamera


def TakePhoto():
    path = 'pics/pinoir.jpg'
    
    #camera.start_preview()
    #time.sleep(1)
    camera.capture(path)
    #camera.stop_preview()
    
    return path

def ReplyWithPhoto(sender):
    print("taking photo...")
    path = TakePhoto()
    print("uploading...")
    media = twitter.upload_media(media=open(path,'rb'))
    pprint.pprint(media)
    print("tweeting...")
    twitter.update_status(status='@' + sender + ' ' + "Cheese!", media_ids=media['media_id_string'])
    #message = str(datetime.now())
    #twitter.send_direct_message(user_id=senderid,screen_name=sender,text=message,media=media['media_id_string'])
    print("done.")

def ReplyWithDean(sender):
    print("gettig dean pic...")
    path = deanpicsfolder + random.choice(deanpics)
    print("uploading...")
    media = twitter.upload_media(media=open(path,'rb'))
    pprint.pprint(media)
    print("tweeting...")
    twitter.update_status(status='@' + sender + ' ' + " Your picture of Dean...", media_ids=media['media_id_string'])
    print("done.")



class MyStreamer(TwythonStreamer):
    

    
    def on_success(self, data):
        if 'text' in data:
            # STATUS UPDATE

            #if 'entities' in data and user_mentions in data['entities'] :

            tweetstring = data['id_str'].encode('utf-8') + ': ' + data['user']['name'].encode('utf-8') + ' [@' + data['user']['screen_name'].encode('utf-8') + '] "' + data['text'].encode('utf-8') + '"'
            print(tweetstring)

            #print(data['text'].encode('utf-8'))    
            #pprint.pprint(data)



            
        elif 'direct_message' in data:
            # DIRECT MESSAGE
            senderid = str(data['direct_message']['sender_id_str'])
            sender = str(data['direct_message']['sender_screen_name'])
            directmessagetext = str(data['direct_message']['text'].encode('utf-8'))
            print("Direct message from " + sender + ' ' + senderid + ' : ' + directmessagetext)
            
            if senderid == andrewpiid:
                # IGNORE
                pass
            #elif senderid == andrewid:
                # FROM ME
                #print(" from me" )
                
            else:
                # FROM ANYOE ELSE
                if (directmessagetext == "photo"):
                    ReplyWithPhoto(sender)
                elif (directmessagetext == "dean"):
                    ReplyWithDean(sender)
                else:
                    #message = str(datetime.now())
                    #twitter.send_direct_message(user_id=senderid,screen_name=sender,text=message,media=media['media_id_string'])

                    pprint.pprint(data)

        elif 'event' in data:
            # EVENT
            if data['event'] == "follow":
                # NEW FOLLOWER
                newFollowerID = data['source']['id_str'].encode('utf-8')
                newFollowerName = data['source']['name'].encode('utf-8')
                newFollowerScreeName = data['source']['screen_name'].encode('utf-8')
                newfollow = 'NEW FOLLOWER: ' + newFollowerName + ' [@' + newFollowerScreeName + '] "' + data['text'].encode('utf-8') + '"'
                print(newfollow)
            else:
                pprint.pprint(data)
        elif 'friends' in data:
            print("Connected...")
        elif 'delete' in data:
            pass
        else:
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

    tokens = [APP_KEY, APP_SECRET, FINAL_OAUTH_TOKEN, FINAL_OAUTH_TOKEN_SECRET]
   
    return tokens




    
    



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


# INIT TWITTER
tokens = Authenticate()
twitter = Twython(tokens[0],tokens[1],tokens[2],tokens[3])
streamer = MyStreamer(tokens[0],tokens[1],tokens[2],tokens[3])

# INIT CAMERA
camera = picamera.PiCamera()
camera.resolution=[640,480]


# INIT DEANPICS
deanpicsfolder = "pics/dean/"
deanpics = listdir(deanpicsfolder)



# START STREAMING

## streamer.statuses.sample()
## streamer.statuses.filter(track='Leeds',language='en',stall_warnings='true', filter_level='medium')
## streamer.user()

streamer.user()

####streamer.statuses.firehose()


    
