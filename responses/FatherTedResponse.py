from Response import Response
import random
class FatherTedResponse(Response):
    def Condition(args, inboxItem):
        return super(FatherTedResponse, args).Condition(inboxItem) \
            and inboxItem.to_me


    def Respond(args, inboxItem):

        responses = [
            # exclaimation
            "WOW!",
            "ROFL!",
            "LOL!",
            "WOWZERS!",
            "OMG!",
            "WTF?!",
            "ZOMG!",
            
            # positive
            "Nice.",
            "Cool.",
            "Hah.",
            "Yeah.",
            "Indeed.",
            "Yes.",
            "Ok.",
            
            # neutral
            "[Shrug]",
            "Wat.",
            "Meh.",
            "Hmpfh.",
            "Whatever.",
            "Whatevs.",

            # questions
            "Who?",
            "Why?",
            "What?",
            "When?",

            # negative
            "No.",
            "Nah.",
            
            # simpsons
            "DOH!",
            "Dont have a cow man!",
             
            # Robot Noises
            "BEEP BOOP."
            
            # father ted
            "That would be an ecumenical matter. #FatherTed",
            "Careful now. #FatherTed",
            "Down with this sort of thing! #FatherTed",
            "Is there anything to be said for another mass? #FatherTed",
            "That money was just resting in my account! #FatherTed",
            "as I said last time, it won't happen again. #FatherTed",
            "These are small... but the ones out there are far away. #FatherTed",
            "I love my brick! #FatherTed",
            "Go away! I don't want to catch menopause! #FatherTed"
        #You'll have some tea...  are you sure you don't want any?  Aw go on,
        #you'll have some.  Go on go on go on go on go on go on go on go on GO
        #ON!
            
            ]
        response = random.choice(responses) 
        return args.ReplyWith(inboxItem, response)

        