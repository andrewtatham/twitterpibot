

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
import threading
import webbrowser

import cv2
import urllib
import numpy as np

import Tkinter

import textwrap

#from textblob import TextBlob

import picamera
def TakePhoto():
    path = "pics/pinoir.jpg"
    #mypicamera.start_preview()
    mypicamera.capture(path) 
    #mypicamera.stop_preview()
    return path




def PicameraTasks():


    while running:
        try:
            #print('Running PicameraTasks: %s' % time.ctime())
            path = TakePhoto()
            image = cv2.imread(path)
            cv2.imshow("picamera", image)
            #cv2.waitKey(1)
            time.sleep(1)

        except Exception as e:

            logging.exception(e.message, e.args)             
            pprint.pprint(e)
   
def WebcamTasks():


    while running:
        try:
            #print('Running WebcamTasks: %s' % time.ctime())
 
            err,image = webcam.read()           
            cv2.imshow("webcam", image)
            #cv2.waitKey(1)
            time.sleep(1)

        except Exception as e:

            logging.exception(e.message, e.args)             
            pprint.pprint(e)
    


def ReplyWithPhoto(sender):
    logging.info("taking photo...")
    path = TakePhoto()
    logging.info("uploading...")
    media = twitter.upload_media(media=open(path,"rb"))
    plogging.info.plogging.info(media)
    logging.info("tweeting...")
    photomessages = ["cheese!", "smile!"]
    twitter.update_status(status="@" + sender + " " + random.choice(photomessages), media_ids=media["media_id_string"])
    #message = str(datetime.now())
    #twitter.send_direct_message(user_id=senderid,screen_name=sender,text=message,media=media["media_id_string"])
    logging.info("done.")

def ReplyWithDean(sender = None, name = None):
    
    if name is None:
        name = random.choice(people)
        
    logging.info("getting " + name + " pic...")
    path = picsfolder + name + "/" + random.choice(pics[name])
    logging.info("uploading " + path + "...")
    media = twitter.upload_media(media=open(path,"rb"))
    logging.info("tweeting...")
    message = random.choice(deanmessages) + " " + name
    
    if sender is not None:
        message = "@" + sender + " " + message 

    twitter.update_status(status= message, media_ids=media["media_id_string"])
    logging.info("done.")

def ReplyWithSong(target, song):
    logging.info("getting " + song + " song...")
    lyrics = songs[song.lower()]
    lastlyric = ""
    for lyric in lyrics:
        lyric = lyric.strip()
        if lyric and lyric != lastlyric:
            tweettext = "@" + target + " " + lyric
            logging.info("tweeting: " + tweettext)
            twitter.update_status(status=tweettext)
            lastlyric = lyric
            time.sleep(1)
            
    
    logging.info("done.")

def RetweetRecursion(data, retweetlevel):
 
    tweetstring = "* " + \
        retweetlevel * 'RT '+ \
        data["user"]["name"] + \
        " [@" + data["user"]["screen_name"] + "] " + \
        data["text"]
    print(tweetstring)
    logging.info(tweetstring)
    

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





def PrintTrends():
    

    #availtrends = twitter.get_available_trends()
    #logging.info(availtrends)
    worldwide_WOEID = 1
    leeds_WOEID = 26042


    worldwide_trends = twitter.get_place_trends(id = worldwide_WOEID)
    #plogging.info.pprint(worldwide_trends)

    leeds_trends = twitter.get_place_trends(id = leeds_WOEID)
    #logging.info(leeds_trends)

    trends = []
    for trend in worldwide_trends[0]["trends"]:
        trendname = trend["name"]
        trends.append(trendname)
    for trend in leeds_trends[0]["trends"]:
        trendname = trend["name"]
        trends.append(trendname)
    print ("Trends...")
    for trend in trends:
        print("")
        print(trend)
        try:
            trendtweets = twitter.search(q = urllib.quote_plus(trend), result_type = "popular")
            for trendtweet in trendtweets["statuses"]:
                print("  " + trendtweet["text"].replace("\n", "   "))
        except Exception as e:   
            logging.exception(e.message, e.args)             
            pprint.pprint(e)


def SuggestedUsers():
    categories = twitter.get_user_suggestions()

    for category in categories:
        print("")
        print(category["name"])
        users = twitter.get_user_suggestions_by_slug(slug = category["slug"])
        #pprint.pprint(users)
        for user in users["users"]:
            #pprint.pprint(user)
            print("")
            print("  " + user["name"])
            print("  @" + user["screen_name"])
            print("  " + user["description"])



def DownloadImage(url):
   
    retval = urllib.urlretrieve(url);
    while(not os.path.isfile(retval[0])):
        time.sleep(0.25)
    return retval[0]
    
    
def ShowImage(path, text):
    if(os.path.isfile(path)):
        image = cv2.imread(path,0)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        scale = 0.75
        origin = (10,10)
        text = textwrap.wrap(text,50)
        for line in text:
            cv2.putText(image,line,origin, font, scale,(0,0,0),3,cv2.CV_AA)
            cv2.putText(image,line,origin, font, scale,(255,255,255),1,cv2.CV_AA)
            origin = (origin[0],origin[1]+18)
        cv2.imshow(windowname, image)
        cv2.waitKey(1)
 
class MyStreamer(TwythonStreamer):

    
    
    def on_success(self, data):
        try:
            if "text" in data:

                logging.info(data)

                andrewpimentioned = False

                tweetid = data["id_str"]

                sender_id = data["user"]["id_str"]
                sender_screen_name = data["user"]["screen_name"]
                tweettext = data["text"]

                if sender_id != andrewpiid:
                    # STATUS UPDATE
                    RetweetRecursion(data, 0)


                #    words = tweettext.split()
                #    # remove non ascii chars
                #    textnoentities = tweettext
                #    textnoentities = ''.join([i if ord(i) < 128 else ' ' for i in textnoentities])                


                    targets = []
                   
                    if "entities" in data:
                        entities = data["entities"]

                        #if "hashtags" in entities:
                        #    hashtags = entities["hashtags"]
                        #    #textnoentities = ReplaceEntity(textnoentities, hashtags, " ")
                                
                        if "urls" in entities:
                            urls = entities["urls"]
                        #    #textnoentities = ReplaceEntity(textnoentities, urls, " ")
                            #for url in urls:
                                #pprint.pprint(url)
                                #print("Opening url " + url["url"])
                                #webbrowser.open(url["url"])
                                
                                

                        if "media" in entities:
                            medias = entities["media"]
                            #pprint.pprint(medias)
                            for media in medias:
                                if media["type"] == "photo":
                                    url = media["media_url"]
                                    #webbrowser.open(url)
                                    path = DownloadImage(url)
                                    ShowImage(path, tweettext)
                                    os.remove(path)
                                    

                        


                            
                            #textnoentities = ReplaceEntity(textnoentities, medias, " ")
                            
                        if "user_mentions" in entities:
                            mentions = entities["user_mentions"]
                            #textnoentities = ReplaceEntity(textnoentities, mentions, " ")
                            for mention in mentions:

                                if mention["screen_name"] != andrewpi and mention["screen_name"] != sender_screen_name:
                                    targets.append(mention["screen_name"])

                            
                                if mention["id_str"] == andrewpiid:
                                    # ANDREWPI MENTION
                                    logging.info("*** ANDREWPI MENTION ***")
                                    andrewpimentioned = True




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
                           

                            if targets.any():
                                ReplyWithSong(targets, word.lower())
                            else:
                                ReplyWithSong(sender, word.lower())
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
                    directmessagetext = str(data["direct_message"]["text"])
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
                            target = sender
                            ReplyWithSong(target, directmessagetext.lower())
                        else:
                            #message = str(datetime.now())
                            #twitter.send_direct_message(user_id=senderid,screen_name=sender,text=message,media=media["media_id_string"])

                            logging.info(data)

                elif "event" in data:
                    # EVENT
                    event = data["event"]
                    sourceID = data["source"]["id_str"]
                    sourceName = data["source"]["name"]
                    sourceScreenName = data["source"]["screen_name"]

                    targetID = data["target"]["id_str"]
                    targetName = data["target"]["name"]
                    targetScreenName = data["target"]["screen_name"]
                
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

def StreamTweets():
    
    # START STREAMING

    ## streamer.statuses.sample()
    ## streamer.statuses.filter(track="Leeds",language="en",stall_warnings="true", filter_level="medium")
    ## streamer.user()

    while running:
        try:       
            streamer.user()
        except Exception as e:
            logging.exception(e.message, e.args)             
            pprint.pprint(e)
 
def HourlyTasks():
    while running:
        try:
            print('Running hourly tasks: %s' % time.ctime())
##            PrintTrends()
##            SuggestedUsers()
            
            time.sleep(60*60)
        except Exception as e:

            logging.exception(e.message, e.args)             
            pprint.pprint(e)
        
def FifteenMinuteTasks():
    while running:
        try:
            print('Running 15min tasks: %s' % time.ctime())
##            PrintTrends()
##            SuggestedUsers()
            
            time.sleep(15*60)
        except Exception as e:

            logging.exception(e.message, e.args)             
            pprint.pprint(e)

def MonitorTasks():
    
    while running:
        try:
            # print('Running monitor tasks: %s' % time.ctime())
            print('')
            time.sleep(15)
        except KeyboardInterrupt:
            print('Exiting: %s' % time.ctime())
            sys.exit(0)



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
    

# INIT SONGS
songsfolder = "songs/"
songs = {}
songfiles = os.listdir(songsfolder)
for songfile in songfiles:
    songname = songfile.lower()
    if songname.endswith('.txt'):
        songname = songname[:-4]
    songs[songname] = open(songsfolder + songfile, "rb").readlines()

##ratelimits = twitter.get_application_rate_limit_status()
###pprint.pprint(ratelimits)
##logging.info(ratelimits)



top = Tkinter.Tk()
cv2.startWindowThread();
cv2.waitKey(1)
thread_list = [
##    threading.Thread(target=MonitorTasks),
##    threading.Thread(target=HourlyTasks),
##    threading.Thread(target=FifteenMinuteTasks),    
    threading.Thread(target=PicameraTasks),    
    threading.Thread(target=WebcamTasks),    
    threading.Thread(target=StreamTweets)]

mypicamera = picamera.PiCamera()
mypicamera.resolution=[640,480]
picamerawindow = cv2.namedWindow("picamera")


# INIT WEBCAM

webcam = cv2.VideoCapture(0)
cv2.namedWindow("webcam")
for i in range(5):
    err,frame = webcam.read()



windowname = "Image"
window = cv2.namedWindow(windowname)


tokens = Authenticate()
twitter = Twython(tokens[0],tokens[1],tokens[2],tokens[3])
time.sleep(0.1)
streamer = MyStreamer(tokens[0],tokens[1],tokens[2],tokens[3])
time.sleep(0.1)

running = True
for thread in thread_list:
    thread.start()
    time.sleep(0.1)



top.mainloop()


print('Exiting: %s' % time.ctime())
running = False

streamer.disconnect()

cv2.destroyWindow(windowname)
cv2.namedWindow("picamera")
cv2.namedWindow("webcam")
cv2.destroyAllWindows()

mypicamera.close()
webcam.release()

for thread in thread_list:
    thread.join() 

print("Done")
