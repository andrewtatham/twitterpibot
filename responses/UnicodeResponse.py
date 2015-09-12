from Response import Response
import random
class UnicodeResponse(Response):
    def __init__(self, *args, **kwargs):


        self.symbols = [
            u"\U00002661", # U+2661 WHITE HEART SUIT
            u"\U00002665", # U+2665 BLACK HEART SUIT
            u"\U00002764", # U+2764 HEAVY BLACK HEART
            u"\U0001F493", # U+1F493 BEATING HEART
            u"\U0001F498", # U+1F498 HEART WITH ARROW
            u"\U0001F497", # U+1F497 GROWING HEART
            u"\U0001F496", # U+1F496 SPARKLING HEART
            u"\U0001F499", # U+1F499 BLUE HEART
            u"\U0001F49A", # U+1F49A GREEN HEART
            u"\U0001F49B", # U+1F49B YELLOW HEART
            u"\U0001F49C" # U+1F49C PURPLE HEART
        ]
        #self.texts = [ unicode(symbol).encode('utf-8') for symbol in self.symbols]

        

    def Condition(args, inboxItem):      
        return super(UnicodeResponse, args).Condition(inboxItem) \
            and inboxItem.to_me \
            and inboxItem.sender.screen_name == "andrewtatham"

    def Respond(args, inboxItem):

        symbol = random.choice(args.symbols)

       
        return args.ReplyWith(inboxItem, text)
