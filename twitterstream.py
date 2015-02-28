

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


from twython import Twython, TwythonStreamer

import time
from datetime import datetime
import pickle
import pprint
import random
import string
import re

from os import listdir
import os.path
import logging
import urllib
#from textblob import TextBlob

##import picamera
##def TakePhoto():
##    path = "pics/pinoir.jpg"
##    camera.capture(path) 
##    return path

##def ReplyWithPhoto(sender):
##    logging.info("taking photo...")
##    path = TakePhoto()
##    logging.info("uploading...")
##    media = twitter.upload_media(media=open(path,"rb"))
##    plogging.info.plogging.info(media)
##    logging.info("tweeting...")
##    twitter.update_status(status="@" + sender + " " + random.choice(photomessages), media_ids=media["media_id_string"])
##    #message = str(datetime.now())
##    #twitter.send_direct_message(user_id=senderid,screen_name=sender,text=message,media=media["media_id_string"])
##    logging.info("done.")

def ReplyWithDean(sender, name):
    logging.info("getting " + name + " pic...")
    path = picsfolder + name + "/" + random.choice(pics[name])
    logging.info("uploading " + path + "...")
    media = twitter.upload_media(media=open(path,"rb"))
    logging.info("tweeting...")
    message = random.choice(deanmessages) + " " + name
    twitter.update_status(status="@" + sender + " " + message, media_ids=media["media_id_string"])
    logging.info("done.")

def ReplyWithSong(target, song):
    logging.info("getting " + song + " song...")
    lyrics = songs[song.lower()]
    lastlyric = ""
    for lyric in lyrics:
        lyric = lyric.strip().encode("utf-8")
        if lyric and lyric != lastlyric:
            tweettext = "@" + target + " " + lyric
            logging.info("tweeting: " + tweettext)
            twitter.update_status(status=tweettext)
            lastlyric = lyric
            time.sleep(1)
            
    
    logging.info("done.")



def RetweetRecursion(data, retweetlevel):

   
    tweetstring = retweetlevel * 'RT ' + data["id_str"].encode("utf-8") + ": " + \
                  data["user"]["name"].encode("utf-8") + \
                  " [@" + data["user"]["screen_name"].encode("utf-8") + "] " \
                  + data["text"].encode("utf-8")  
    logging.info(tweetstring.decode("utf-8"))

    #if "retweeted_status" in data:
    #    if data["retweeted_status"] is not None:
    #        RetweetRecursion(data["retweeted_status"], retweetlevel + 1)


#def ReplaceEntity(text, entities, replacewith):
#    for entity in entities:
        
#        indices = entity["indices"]
#        beginindex = indices[0]
#        endindex = indices[1]
#        length = endindex - beginindex
        
#        text = text[:beginindex] + replacewith * length + text[endindex:]
#    return text



#def ReplaceWordsWithList(text, tags, types, wordlist):
#    retval = text
#    for tag in tags:
#        if tag[1] in types:
#            retval = retval.replace(tag[0], random.choice(wordlist))
#    return retval

class MyStreamer(TwythonStreamer):

    
    
    def on_success(self, data):
        try:
            if "text" in data:

                andrewpimentioned = False

                tweetid = data["id_str"].encode("utf-8")

                sender_id = data["user"]["id_str"]
                sender_screen_name = data["user"]["screen_name"]
                tweettext = data["text"].encode("utf-8")

                if sender_id != andrewpiid:
                    # STATUS UPDATE
                    RetweetRecursion(data, 0)


                #    words = tweettext.split()
                #    # remove non ascii chars
                #    textnoentities = tweettext
                #    textnoentities = ''.join([i if ord(i) < 128 else ' ' for i in textnoentities])                


                #    targets = []
                   
                #    if "entities" in data:
                #        entities = data["entities"]

                #        if "hashtags" in entities:
                #            hashtags = entities["hashtags"]
                #            textnoentities = ReplaceEntity(textnoentities, hashtags, " ")
                                
                #        if "urls" in entities:
                #            urls = entities["urls"]
                #            textnoentities = ReplaceEntity(textnoentities, urls, " ")

                #        if "media" in entities:
                #            medias = entities["media"]
                #            textnoentities = ReplaceEntity(textnoentities, medias, " ")
                            
                #        if "user_mentions" in entities:
                #            mentions = entities["user_mentions"]
                #            textnoentities = ReplaceEntity(textnoentities, mentions, " ")
                #            for mention in mentions:

                #                if mention["screen_name"] != andrewpi and mention["screen_name"] != sender_screen_name:
                #                    targets.append(mention["screen_name"])

                            
                #                if mention["id_str"] == andrewpiid:
                #                    # ANDREWPI MENTION
                #                    logging.info("*** ANDREWPI MENTION ***")
                #                    andrewpimentioned = True




                ## remove any remaining urls                
                ## textnoentities = re.sub(r'^https?:\/\/.*[\r\n]*', '', textnoentities)


                #logging.info("textinitial = " + tweettext)
                #logging.info("textnoentities = " + textnoentities)

                #wiki = TextBlob(textnoentities)
                #logging.info(wiki.tags)

                #types = ["NN","NNS","NNP","NNPS"]
                #newtext = ReplaceWordsWithList(tweettext, wiki.tags, types, fruitlist)
                #logging.info("newtext = " + newtext)
                
                if andrewpimentioned:

                    for word in words:
                        if (word.lower() == "photo"):
                            ReplyWithPhoto(sender)
                        elif (word.lower() in pics):
                            ReplyWithDean(sender, word.lower())
                        elif word.lower() in songs:
                            # TODO parse tharget from message
                            if targets.any():
                                ReplyWithSong(targets, word.lower())
                            else:
                                ReplyWithSong(target, word.lower())
                        else:
                            pass


                    trend = random.choice(trends)

                    replytext = "@" + sender_screen_name + " " + newtext + " " + trend


                    
                    twitter.update_status(status=replytext, 
                                          in_reply_to_status_id=tweetid)


                
                elif "direct_message" in data:
                    # DIRECT MESSAGE
                    senderid = str(data["direct_message"]["sender_id_str"])
                    sender = str(data["direct_message"]["sender_screen_name"])
                    directmessagetext = str(data["direct_message"]["text"].encode("utf-8"))
                    logging.info("Direct message from " + sender + " " + senderid + " : " + directmessagetext)
                
                    if senderid == andrewpiid:
                        # IGNORE
                        pass
                    #elif senderid == andrewid:
                        # FROM ME
                        #logging.info(" from me" )
                    
                    else:
                        # FROM ANYOE ELSE
    ##                    if (directmessagetext.lower() == "photo"):
    ##                        ReplyWithPhoto(sender)
    ##                    elif (directmessagetext.lower() in pics):
                        if (directmessagetext.lower() in pics):
                            ReplyWithDean(sender, directmessagetext.lower())
                        elif  directmessagetext.lower() in songs:
                            # TODO parse tharget from message
                            target = andrew + ' @' + markr + ' @' + jamie
                            ReplyWithSong(target, directmessagetext.lower())
                        else:
                            #message = str(datetime.now())
                            #twitter.send_direct_message(user_id=senderid,screen_name=sender,text=message,media=media["media_id_string"])

                            logging.info(data)

                elif "event" in data:
                    # EVENT
                    event = data["event"]
                    sourceID = data["source"]["id_str"].encode("utf-8")
                    sourceName = data["source"]["name"].encode("utf-8")
                    sourceScreenName = data["source"]["screen_name"].encode("utf-8")

                    targetID = data["target"]["id_str"].encode("utf-8")
                    targetName = data["target"]["name"].encode("utf-8")
                    targetScreenName = data["target"]["screen_name"].encode("utf-8")
                
                    eventinfo = "EVENT: " + event \
                                + " SOURCE: " + sourceName + " [" + sourceScreenName + "]" \
                                + " TARGET: " + targetName + " [" + targetScreenName + "]"
                    logging.info(eventinfo)
                
                    if data["event"] == "follow":
                        # NEW FOLLOWER
                        pass
                    elif data["event"] == "unfollow":
                        # UNFOLLOW
                        pass
                    else:
                        logging.info(data)
                elif "friends" in data:
                    logging.info("Connected...")
                elif "delete" in data:
                    pass
                else:
                    logging.info(data)
        except Exception as e:   
            logging.exception(e.message, e.args)             
            pprint.pprint(e)

            
    def on_error(self, status_code, data):
         
        msg = str(status_code)  + " " + data
        logging.error(msg)
        print(msg)





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




    
    


logging.basicConfig(filename='twitter.log',level=logging.INFO)


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
time.sleep(1)
streamer = MyStreamer(tokens[0],tokens[1],tokens[2],tokens[3])
time.sleep(1)

# INIT CAMERA
##photomessages = ["cheese!", "smile!"]
##camera = picamera.PiCamera()
##camera.resolution=[640,480]


# INIT DEANPICS


deanmessages = ["need moar", "many", "so much", "very", "wow"]
picsfolder = "pics/"
if not os.path.exists(picsfolder):
    os.makedirs(picsfolder)
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
    
    
##  logging.info(songs)
    
#TODO Split singular and plural
###fruitlist = ["Apple",
###        "Apricots",
###        "Avocado",
###        "Banana",
###        "Blackberry",
###        "Blueberries",
###        "Cherries",
###        "Coconut",
###        "Cranberry",
###        "Cucumber",
###        "Dates",
###        "Fig",
###        "Gooseberry",
###        "Grapefruit",
###        "Grapes",
###        "Kiwi",
###        "Kumquat",
###        "Lemon",
###        "Lime",
###        "Lychee",
###        "Mango",
###        "Melon",
###        "Nectarine",
###        "Orange",
###        "Papaya",
###        "Passion Fruit",
###        "Peach",
###        "Pear",
###        "Pineapple",
###        "Plum",
###        "Pomegranate",
###        "Clementine",
###        "Prunes",
###        "Raspberries",
###        "Strawberries",
###        "Tangerine",
###        "Watermelon"]



##ratelimits = twitter.get_application_rate_limit_status()
##logging.info(ratelimits)





#availtrends = twitter.get_available_trends()
#logging.info(availtrends)
worldwide_WOEID = 1
leeds_WOEID = 26042




worldwide_trends = twitter.get_place_trends(id = worldwide_WOEID)
#plogging.info.pprint(worldwide_trends)

leeds_trends = twitter.get_place_trends(id = leeds_WOEID)
#logging.info(leeds_trends)

trends = []
trendstweets = dict()
for trend in worldwide_trends[0]["trends"]:
    trendname = trend["name"]
    trends.append(trendname)
for trend in leeds_trends[0]["trends"]:
    trendname = trend["name"]
    trends.append(trendname)
print ("Trends...")
for trend in trends:
    print(trend)
    
for trend in trends:  
    trendtweets = twitter.search(q = urllib.quote_plus(trend), result_type = "popular")
    trendstweets.update(trend,trendtweets)

for trend in trends:
    print(trend)
    pprint.pprint(trendstweets[trend])    


print ("User Suggestions...")
user_suggestions = twitter.get_user_suggestions()
for user_suggestion in user_suggestions:
    pprint.pprint(user_suggestion)



# START STREAMING

## streamer.statuses.sample()
## streamer.statuses.filter(track="Leeds",language="en",stall_warnings="true", filter_level="medium")
## streamer.user()

streamer.user()

####streamer.statuses.firehose()


    
