
from InboxTextItem import InboxTextItem

import HTMLParser
import logging
from itertools import cycle
from colorama import Fore, Style
import random
import Users
import Identity

#import nltk
h = HTMLParser.HTMLParser()

tweetcolours = cycle([Fore.GREEN, Fore.YELLOW])
trendcolours = cycle([Fore.MAGENTA, Fore.WHITE])
searchcolours = cycle([Fore.CYAN, Fore.WHITE])



class IncomingTweet(InboxTextItem):
    def __init__(self, data):
        # https://dev.twitter.com/overview/api/tweets
        # logging.info(data)

        super(IncomingTweet, self).__init__(data)

        self.isTweet = True
        self.status_id = data["id_str"]
        self.sender = Users.getUser(data = data["user"])
        self.from_me = self.sender.isMe
        self.favorited = bool(data["favorited"])
        self.retweeted = bool(data["retweeted"])       
        self.source = None
        self.sourceIsTrend = False
        self.sourceIsSearch = False
        if 'tweetsource' in data:
            self.source = data['tweetsource']
            if 'trend' in self.source:
                self.sourceIsTrend = True
            elif 'search' in self.source:
                self.sourceIsSearch = True

        logging.debug(data["text"])
        self.text = h.unescape(data["text"])


        self.words = self.text.split()
        
        self.to_me = False
        self.targets = []                  
        if "entities" in data:
            entities = data["entities"]
                            
            if "user_mentions" in entities:
                mentions = entities["user_mentions"]
                for mention in mentions:
                    if mention["id_str"] != Identity.id: #and mention["screen_name"] != self.sender_screen_name:
                        self.targets.append(mention["screen_name"])
                      
                    if mention["id_str"] == Identity.id:
                        self.to_me = True

        #self.tokens = nltk.word_tokenize(self.text)

        #self.tags = nltk.pos_tag(self.tokens)

        #self.entities =nltk.chunk.ne_chunk(self.tags)


    def Display(args):
        colour = ""
        text = ""
        if args.source:
            text += '['+ args.source + '] '
            if args.sourceIsTrend:
                colour = trendcolours.next()
            elif args.sourceIsSearch:
                colour = searchcolours.next()
        else:
            colour = tweetcolours.next()
            text += "* "

        text += args.sender.name + ' [@' + args.sender.screen_name + '] ' + args.text.replace('\n',' ')
    
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
 
        