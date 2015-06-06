
from InboxTextItem import InboxTextItem

import HTMLParser

h = HTMLParser.HTMLParser()

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

        self.mentioned = False

        self.status_id = data["id_str"]

        self.sender_id = data["user"]["id_str"]
        self.sender_name = data["user"]["name"]
        self.sender_screen_name = data["user"]["screen_name"]
        #self.sender_description = data["user"]["description"]
        #self.sender_profile_image_url = data["user"]["profile_image_url"]
        #self.sender_profile_banner_url = data["user"]["profile_banner_url"]

        self.tweettextraw = data["text"].replace('\u2026','')                
        self.text = h.unescape(self.tweettextraw.decode('utf-8', 'ignore'))
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
                        # ANDREWPI MENTION
                        print("*** ANDREWPI MENTION ***")
                        logging.info("*** ANDREWPI MENTION ***")
                        self.mentioned = True
                
    def NeedsReply(self):
        return not self.from_me and self.mentioned

    def Display(args):
        
        text = args.text
        print(text)


