
from InboxTextItem import InboxTextItem

import HTMLParser
import logging
from itertools import cycle
from colorama import Fore, Style
import random


h = HTMLParser.HTMLParser()

colours = cycle([
            Fore.GREEN,
            Fore.YELLOW
                   ])


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


class IncomingTweet(InboxTextItem):
    def __init__(self, data):
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
        
        self.from_me = self.sender_id == andrewpiid
        self.targets = []

                   
        if "entities" in data:
            entities = data["entities"]
                            
            if "user_mentions" in entities:
                mentions = entities["user_mentions"]
                for mention in mentions:
                    if mention["screen_name"] != andrewpi and mention["screen_name"] != self.sender_screen_name:
                        self.targets.append(mention["screen_name"])
                      
                    if mention["id_str"] == andrewpiid:
                        self.to_me = True
                


    def Display(args):
        
        text = "* " + args.sender_name + ' [@' + args.sender_screen_name+ '] ' + args.text
        



        colour = colours.next()

     
        if args.to_me:
            colour += Style.BRIGHT
        elif args.from_me:
            colour += Style.NORMAL
        else:
            colour += Style.DIM



        print(colour + text.encode("utf-8"))
 

 
        