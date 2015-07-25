
from InboxTextItem import InboxTextItem

import HTMLParser
import logging
from itertools import cycle
from colorama import Fore, Style
import random
#import nltk

h = HTMLParser.HTMLParser()

tweetcolours = cycle([
            Fore.GREEN,
            Fore.YELLOW
                   ])




class IncomingTweet(InboxTextItem):
    def __init__(self, data, context):
        # https://dev.twitter.com/overview/api/tweets
        #logging.info(data)

        super(IncomingTweet, self).__init__(data)

        self.isTweet = True
        self.to_me = False

        self.status_id = data["id_str"]

        self.sender_id = data["user"]["id_str"]
        self.sender_name = data["user"]["name"]
        self.sender_screen_name = data["user"]["screen_name"]
        #self.sender_description = data["user"]["description"]
        #self.sender_profile_image_url = data["user"]["profile_image_url"]
        #self.sender_profile_banner_url = data["user"]["profile_banner_url"]


        logging.info(data["text"])
        self.text = h.unescape(data["text"])


        self.words = self.text.split()
        
        self.from_me = self.sender_id == context.users.me["id"]
        self.targets = []

                   
        if "entities" in data:
            entities = data["entities"]
                            
            if "user_mentions" in entities:
                mentions = entities["user_mentions"]
                for mention in mentions:
                    if mention["screen_name"] != context.users.me["id"] and mention["screen_name"] != self.sender_screen_name:
                        self.targets.append(mention["screen_name"])
                      
                    if mention["id_str"] == context.users.me["id"]:
                        self.to_me = True
                




    


        #self.tokens = nltk.word_tokenize(self.text)

        #self.tags = nltk.pos_tag(self.tokens)

        #self.entities =nltk.chunk.ne_chunk(self.tags)


    def Display(args):
        
        text = "* " + args.sender_name + ' [@' + args.sender_screen_name+ '] ' + args.text
        



        colour = tweetcolours.next()

     
        if args.to_me:
            colour += Style.BRIGHT
        elif args.from_me:
            colour += Style.NORMAL
        else:
            colour += Style.DIM



        print(colour + text.encode("utf-8"))
 
        #print(Fore.MAGENTA + str(args.tokens))
        #print(Fore.CYAN + str(args.tags))
        #print(Fore.WHITE + str(args.entities))
 
        