from Response import Response
import random
class FatherTedResponse(Response):
    def Condition(args, inboxItem):
        return super(FatherTedResponse, args).Condition(inboxItem) and inboxItem.to_me

    def Respond(args, inboxItem):


        #You'll have some tea... are you sure you don't want any? Aw go on, you'll have some. Go on go on go on go on go on go on go on go on GO ON!

        responses = [
            "That would be an ecumenical matter",
            "Careful now",
            "Down with this sort of thing",
            "Is there anything to be said for another mass?",
            "That money was just resting in my account!",
            "as I said last time, it won't happen again",
            "These are small... but the ones out there are far away.",
            "I love my brick!",
            "Go away! I don't want to catch menopause!"
            ]
        response = random.choice(responses) + " #FatherTed"
        return args.ReplyWith(inboxItem, response)

        