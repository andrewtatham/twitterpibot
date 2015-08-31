from Response import Response
import random
class LoveResponse(Response):
    def __init__(self, *args, **kwargs):
        self.texts = [u"\u2661", # U+2661 WHITE HEART SUIT
            u"\u2665", # U+2665 BLACK HEART SUIT
            u"\u2764", # U+2764 HEAVY BLACK HEART
            u"\U0001F493", # U+1F493 BEATING HEART
            u"\U0001F498", # U+1F498 HEART WITH ARROW
            u"\U0001F497", # U+1F497 GROWING HEART
            u"\U0001F496", # U+1F496 SPARKLING HEART
            u"\U0001F499", # U+1F499 BLUE HEART
            u"\U0001F49A", # U+1F49A GREEN HEART
            u"\U0001F49B", # U+1F49B YELLOW HEART
            u"\U0001F49C" # U+1F49C PURPLE HEART
        ]



    def Condition(args, inboxItem):
        return False
        #return super(LoveResponse, args).Condition(inboxItem) \
        #    and inboxItem.to_me \
        #    and inboxItem.sender_screen_name in args.infatuations



        
    

    def Respond(args, inboxItem):
        text = u"I " + random.choice(args.texts) + u" U"
        return args.ReplyWith(inboxItem, text.encode('utf-8'))
