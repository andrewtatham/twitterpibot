import random
import time

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

how_are_you_responses = [

    "I'm SUPER! Thanks for asking!",
    "Fair to middlin'",
    "Can't complain",
    "I'm fine. How are you?",
    "I'm as well as can be.",
    "I'm trying really hard to avoid ambiguous questions at the moment.",
    "How are you?",
    "I could complain, but I'm not going to.",
    "Upright and still breathing.",
    "Thanks for caring babe! Glad to be here with you.",
    "Better than yesterday, but not as good as I will be tomorrow!",
    "I am.",
    "Wondering how you are.",
    "Strange, and getting stranger.",
    "My usual Devil-may-care self.",
    "I'm endeavoring to persevere.",
    "How am I what?",
    "Not so hot, but nothing a stiff drink and some girl talk couldn't fix.",
    "How do you think I am?",
    "Do you want the short version or the long one?",
    "Eh, you win some you lose some.",
    "I'll leave that up to your imagination.",
    "Shhhhh. It's a secret.",
    "I'll let you know when I figure it out.",
    "Taking deep breaths.",
    "Ready for tomorrow.",
    "To tell you the truth, my ______ hurts, but my doc's working on a solution for me so I'm hopeful.",
    "I've been better.",
    "Trying to stay positive.",
    "Who wants to know?",
    "Not my best day, but not my worst day, either.",
    "Let's just say less than super.",
    "Wouldn't you like to know!",
    "I'm taking it easy.",
    "Staying grounded.",
    "(bunch of grunts, gurgles, and other random noises) pssh, fft, mmhm, ya know?",
    "Trying to mix the good in with the bad, you know?",
    "I don't know.",
    "Give me a chocolate bar and I'll be fantastic!",
    "Ready for a nap.",
    "Does it matter? I'm a babe no matter what ;)",
    "Not in the mood to discuss how I feel, but thanks for asking, it really helps to know you care.",
    "Somewhere between blah and meh.",
    "I put pants on, didn't I?",
    "Hold on, let me get the sleep out of my eyes.",
    "Just hug me and leave it at that.",
    "I could really go for a back massage!",
    "Same old, same old.",
    "I could really go for a walk, want to join me?",
    "(If you have the time) Let's make some tea and talk about it.",
    "Ready for my meds. :D",
    "Trying to come out on top.",
    "In need of some peace and quiet.",
    "Get back to me on that.",
    "Oooooohhhmmmm.",
    "Under construction.",
    "Looking to put some pep back in my step.",
    "Thinking about getting away from it all...want to plan a mini-vacation?",
    "Improving.",
    "I'm trying to be a big girl about all of this.",
    "Mama said there'd be days like this, there'd be days like this, my mama said.",
    "Instead of waking up on the wrong side of the bed, I think I woke up underneath it.",
    "Remembering to stay patient.",
    "Trying not to burst into tears. I get an A for effort, right?",
    "In need of some me-time.",
    "I feel like crap! Know any good jokes to cheer me up?",
    "Taking all the love and support I can get, thanks!",
    "As happy as a clam, a clam that's been cracked open, doused in lemon and shot down the gullet.",
    "Appreciating the things I have.",
    "Getting there.",
    "On a scale of one to punching someone in the face?",
    "In desperate need of a mani/pedi.",
    "Somewhere between drab and fab.",
    "Things are bound to get better, yes?",
    "Not giving up.",
    "Getting stronger.",
    "Learning.",
    "Rolling with the punches.",
    "You can't know pleasure without pain, right? :)",
    "In a give-no-shits, take-no-prisoners kind of mood.",
    "I get knocked down, but I get up again!",
    "Gearing up for a comeback. I'll keep you posted on my progress.",
    "Rooting for the underdog (me).",
    "Gotta keep on keepin' on.",
    "I've seen better days.",
    "If I was an animal right now, I'd probably be a sloth (or a turtle).",
    "Ready for you to make a goofy face/ make me laugh/ make me smile.",
    "Do you want to join me in a nice long, relaxing scream? AAARRRGGHHHH",
    "I mean, I'm not doing jumping jacks or back flips, but I'm here.",
    "You can't win 'em all.",
    "Imagining myself on a beach far away.",
    "Crazy. sdhjMhj kljdghpe'sh;g'ep; ea'khg sdjhm, right?",
    "I'm feeling more like Oscar the Grouch than Elmo right now.",
    "I feel like crap, but doing the best I can. Tomorrow's another day, yeah?",
    "I'm feeling really grateful for this beautiful day.",
    "Better now that you're here ;)",
    "I don't feel that great, but my hair looks awesome, right?",
    "Today I'm more CHRONIC than BABE.",
    "Not so hot. Wanna help distract me by telling me about your day?",
    "Keepin' busy, which is a good distraction from my other tough stuff.",
    "I'll be better when ______ gets fixed, but for now I'm doin' OK. Thanks!",
    "I'm glad to see you! What's new? ",
    "I'm giving her all she's got, Captain!"
]

HelloWords = [
    "Hi",
    "Hiya",
    "Hey",
    "Hello",
    "Howdy",
    "Yo",
    "Bonjour",
    "G'day"
]

weather_responses = [
    "Red sky at night, shepherd's delight. Red sky in the morning, shepherd's warning",
    "When the wind is out of the East, tis never good for man nor beast",
    "When halo rings Moon or Sun, rain's approaching on the run",
    "Mackerel sky and mare's tails make tall ships carry low sails",
    "Rain before seven, fine by eleven",
    "If crows fly low, winds going to blow; If crows fly high, winds going to die.",
    "Whether it's cold or whether it's hot; We shall have weather, whether or not!",
    "No weather is ill, if the wind is still",
    "Rain, rain go away; come back another day"
]

weekend_past_responses = [
    "It was awesome!",
    "It was pretty laid-back",
    "I went out with some friends on Saturday",
    "I just puttered around the house",
    "I had a pretty uneventful weekend",
    "I had a night in",
    "I stayed at home",
    "I cleaned up all day",
    "I tidied up my bedroom",
    "I stayed in and read a book",
    "I slept in",
    "I slept longer than I usually do",
    "I lay in bed all morning",
    "I spent the whole weekend studying",
    "I did some gardening",
    "I just chilled out at home",
    "I took it easy",
    "I had friends over for dinner",
    "I just flicked through my iPod and put on some songs",
    "I had a great night out",
    "I met up with friends.",
    "I caught up with friends",
    "I saw a film",
    "I bumped into an old school friend",
    # (= it wasn't planned, it just happened while I was walking down the street or going shopping)
    "I ran into an old work colleague",
    "I got drunk",  # | hammered | smashed | trashed | wasted (slang for you drank a lot and was very drunk)
    "I went out"
    "I went out with a bunch of friends"
    "I went away for the weekend",
    "I went to a yoga class",
    "I went to the opera",
    "I went to the cinema",
    "I went to the theatre",
    "I went to the pub",
    "I went clubbing",
    "I went shopping",
    "I went bowling"
]

weekend_future_responses = [
    "I'm driving to Baltimore with a friend",
    "I've got a date lined up,",
    "Francine and I are taking the kids to the zoo",
    "I don't have anything planned",
    "I'll probably just stay at home and relax",
    "I just want to sleep in!"



    # go out to eat
    # go out (to a bar or club)
    # see a movie
    # binge watch TV shows
    # chill out at home
    # sleep in
    # catch up on sleep
    # sleep in
    # lay around the house
    # do some housework
    # do some yard work
    # spend time with your family
    # take a road trip
    # go to church
    # get together with friends
    # have a cookout
    # have a house party
    # have a dinner party
    # have a big family meal
    # go shopping
    # catch up on work
]

levels = {
    0: {
        "How are you?": how_are_you_responses,
        "How are you today?": how_are_you_responses,
        "How's tricks?": how_are_you_responses,
        "How ya diddlin'?": how_are_you_responses,

        "How's the weather where you are?": weather_responses,
        "So what about all this weather we've been having?": weather_responses

    },
    1: {

        "How did you spend the weekend?": weekend_past_responses,
        "Did you do anything special?": weekend_past_responses,
        "How was your weekend?": weekend_past_responses,
        "Did you do anything fun over the weekend?": weekend_past_responses,
        "What did you get up to this weekend?": weekend_past_responses,
        "Did you have a good weekend?": weekend_past_responses,

        "What are you doing this weekend?": weekend_future_responses,
        "Do you have anything going on this weekend?": weekend_future_responses,
        "Do you have any big plans for the weekend?": weekend_future_responses,
        "Do you have anything planned for this weekend?": weekend_future_responses,

        # news topics

        # "What's your favorite book?": [],
        # "Who would you bet on to win the Superbowl this year?": [],
        # "Do you have any interesting hobbies?": [],
        # "I love watersports, they're my passion. How about you?": [],
        # "What's your favorite holiday?": [],
        # "If you could go back in time, to what time period would you travel?": [],
        # "What would you do if you won the lottery tomorrow?": [],
        # "If you were about to be stranded on a desert island and could bring one person with you, who would it be?": [],
        # "You just found a genie in a bottle. What would your three wishes be?": [],
        # "Aliens just landed and want you to share with them the five best foods in the world. What would you give them to try out?": [],
        # "If a movie was made about your life, what famous actor or actress would play you?": []
    }

}


def get_prompt(level):
    return random.choice(levels[level])


def get_response(level, prompt):
    if level in levels:
        if prompt in levels[level]:
            responses = levels[level][prompt]
            return random.choice(responses)
        else:
            return get_prompt(level)
    else:
        return get_prompt(0)


class ConversationScheduledTask(ScheduledTask):
    def __init__(self, identity, converse_with_identity):
        super(ConversationScheduledTask, self).__init__(identity)
        self._converse_with = converse_with_identity

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(13, 25), minutes=random.randint(0, 59))

    def on_run(self):
        reply_to_id = None
        for level in range(0, 1):
            prompt = get_prompt(level)
            reply_to_id = self.identity.twitter.send(
                OutgoingTweet(text=".@" + self._converse_with.screen_name + " " + prompt,
                              in_reply_to_status_id=reply_to_id))
            time.sleep(5)

            response = get_response(level, prompt)
            reply_to_id = self._converse_with.twitter.send(
                OutgoingTweet(text=".@" + self.identity.screen_name + " " + response,
                              in_reply_to_status_id=reply_to_id))
            time.sleep(5)


if __name__ == "__main__":
    import main

    admin = None
    one = main.AndrewTathamPiIdentity(admin)
    two = main.AndrewTathamPi2Identity(admin)

    task = ConversationScheduledTask(one, two)
    task.on_run()
