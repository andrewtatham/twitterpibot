

# features/fixes

# Error handling
# mentions/retweets

# image ocr/ai
# some neural network shit


# discover feed
# trends
# hashtags
# followfriday
# tits teusday

# weather
# BBC breaking news
# celebrity/verified acc

# word replacement

# word/insult of the day

# song lyrics
# boh rap
# ice baby
# 5000 miles


from twython import Twython, TwythonStreamer

import time
from datetime import datetime
import pickle
import pprint
import random
import string

from os import listdir
import os.path


##import picamera
##def TakePhoto():
##    path = "pics/pinoir.jpg"
##    camera.capture(path) 
##    return path

##def ReplyWithPhoto(sender):
##    print("taking photo...")
##    path = TakePhoto()
##    print("uploading...")
##    media = twitter.upload_media(media=open(path,"rb"))
##    pprint.pprint(media)
##    print("tweeting...")
##    twitter.update_status(status="@" + sender + " " + random.choice(photomessages), media_ids=media["media_id_string"])
##    #message = str(datetime.now())
##    #twitter.send_direct_message(user_id=senderid,screen_name=sender,text=message,media=media["media_id_string"])
##    print("done.")

def ReplyWithDean(sender, name):
    print("getting " + name + " pic...")
    path = picsfolder + name + "/" + random.choice(pics[name])
    print("uploading " + path + "...")
    media = twitter.upload_media(media=open(path,"rb"))
    pprint.pprint(media)
    print("tweeting...")
    message = random.choice(deanmessages) + " " + name
    twitter.update_status(status="@" + sender + " " + message, media_ids=media["media_id_string"])
    print("done.")

def ReplyWithSong(target, song):
    print("getting " + song + " song...")
    lyrics = songs[song.lower()]
    lastlyric = ""
    for lyric in lyrics:
        lyric = lyric.strip().encode("utf-8")
        if lyric and lyric != lastlyric:
            print("tweeting: " + lyric)

            twitter.update_status(status="@" + target + " " + lyric)
            lastlyric = lyric
            time.sleep(1)
            
    
    print("done.")



def RetweetRecursion(data, retweetlevel):

   
    tweetstring = retweetlevel * 'RT ' + data["id_str"].encode("utf-8") + ": " + data["user"]["name"].encode("utf-8") + " [@" + data["user"]["screen_name"].encode("utf-8") + "] " + data["text"].encode("utf-8")  
    print(tweetstring)

    if "retweeted_status" in data:
        if data["retweeted_status"] is not None:
            RetweetRecursion(data["retweeted_status"], retweetlevel + 1)

class MyStreamer(TwythonStreamer):

    
    
    def on_success(self, data):
        try:
            if "text" in data:
                # STATUS UPDATE

                if data["user"]["id_str"] == andrewid:
                    pprint.pprint(data)
                

##                if "entities" in data:
##                    entities = data["entities"]
##
##                    if "user_mentions" in entities:
##                        mentions = entities["user_mentions"]
##                        for mention in mentions:
##                            if mention["id_str"] == andrewpiid:
##                                # ANDREWPI MENTION
                                
                                
                
                RetweetRecursion(data, 0)
                


                
            elif "direct_message" in data:
                # DIRECT MESSAGE
                senderid = str(data["direct_message"]["sender_id_str"])
                sender = str(data["direct_message"]["sender_screen_name"])
                directmessagetext = str(data["direct_message"]["text"].encode("utf-8"))
                print("Direct message from " + sender + " " + senderid + " : " + directmessagetext)
                
                if senderid == andrewpiid:
                    # IGNORE
                    pass
                #elif senderid == andrewid:
                    # FROM ME
                    #print(" from me" )
                    
                else:
                    # FROM ANYOE ELSE
##                    if (directmessagetext.lower() == "photo"):
##                        ReplyWithPhoto(sender)
##                    elif (directmessagetext.lower() in pics):
                    if (directmessagetext.lower() in pics):
                        ReplyWithDean(sender, directmessagetext.lower())
                    elif  directmessagetext.lower() in songs:
                        target = andrew + ' @' + markr + ' @' + jamie
                        ReplyWithSong(target, directmessagetext.lower())
                    else:
                        #message = str(datetime.now())
                        #twitter.send_direct_message(user_id=senderid,screen_name=sender,text=message,media=media["media_id_string"])

                        pprint.pprint(data)

            elif "event" in data:
                # EVENT
                event = data["event"]
                sourceID = data["source"]["id_str"].encode("utf-8")
                sourceName = data["source"]["name"].encode("utf-8")
                sourceScreenName = data["source"]["screen_name"].encode("utf-8")

                targetID = data["target"]["id_str"].encode("utf-8")
                targetName = data["target"]["name"].encode("utf-8")
                targetScreenName = data["target"]["screen_name"].encode("utf-8")
                
                eventinfo = "EVENT: " + event + " SOURCE: " + sourceName + " [" + sourceScreenName + "] TARGET: " + targetName + " [" + targetScreenName + "]"
                print(eventinfo)
                
                if data["event"] == "follow":
                    # NEW FOLLOWER
                    pass
                elif data["event"] == "unfollow":
                    # UNFOLLOW
                    pass
                else:
                    pprint.pprint(data)
            elif "friends" in data:
                print("Connected...")
            elif "delete" in data:
                pass
            else:
                pprint.pprint(data)
        except Exception as e:                
            pprint.pprint(e)

            
    def on_error(self, status_code, data):

            print(str(status_code)  + " " + data)





def Authenticate():
    
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




    
    



andrewpi = "andrewtathampi" 
andrewpiid = "2935295111"

andrew = "andrewtatham"
andrewid = "19201332"

helen = "morris_helen"
markr = "fuuuunnnkkytree"
jamie = "jami3rez"
dean = "dcspamoni"
chriswatson = "watdoghotdog"
fletch = "paulfletcher79"
simon = "Tolle_Lege"

users = [andrew, markr, jamie, helen, dean, chriswatson, simon]


# INIT TWITTER
tokens = Authenticate()
twitter = Twython(tokens[0],tokens[1],tokens[2],tokens[3])
streamer = MyStreamer(tokens[0],tokens[1],tokens[2],tokens[3])

# INIT CAMERA
##photomessages = ["cheese!", "smile!"]
##camera = picamera.PiCamera()
##camera.resolution=[640,480]


# INIT DEANPICS


deanmessages = ["need moar", "many", "so much", "very", "wow"]
picsfolder = "pics/"
pics = {}
people = os.listdir(picsfolder)
for person in people:
    name = str(person)
    personpicsfolder = picsfolder + name + "/"
    if os.path.isdir(personpicsfolder):
        pics[name] = os.listdir(personpicsfolder)
    
#pprint.pprint(people)
#for person in people:
#    name = str(person)
#    print(name)
#    pprint.pprint(pics[name])





# INIT SONGS
songsfolder = "songs/"
songs = {}
songfiles = os.listdir(songsfolder)
for songfile in songfiles:
    songname = songfile.lower()
    if songname.endswith('.txt'):
        songname = songname[:-4]
    songs[songname] = open(songsfolder + songfile, "rb").readlines()
    
    
pprint.pprint(songs)
#for person in people:
#    name = str(person)
#    print(name)
#    pprint.pprint(pics[name])


# START STREAMING

## streamer.statuses.sample()
## streamer.statuses.filter(track="Leeds",language="en",stall_warnings="true", filter_level="medium")
## streamer.user()

streamer.user()

####streamer.statuses.firehose()


    
