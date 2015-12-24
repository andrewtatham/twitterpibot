import random

how_are_you_responses = [

    "I'm SUPER! Thanks for asking!",
    "Fair to middlin'",
    "Can't complain",

    "I'm fine. How are you?",
    "I'm as well as can be.",
    "I'm trying really hard to avoid ambiguous questions at the moment.",
    "(Just answer with the same question:) How are you?",
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
    "I feel like crap! Know any good dirty jokes to cheer me up?",
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

general_prompts = \
    {
        "How are you?": how_are_you_responses,
        "How are you today?": how_are_you_responses,
        "Hows tricks?": how_are_you_responses,
        "How ya diddlin'?": how_are_you_responses,
        "Hows the weather where you are?": weather_responses,
        "So what about all this weather we've been having?": weather_responses
    }

prompts = {}
prompts.update(general_prompts)

prompts_list = [str(key) for key in prompts.keys()]
prompts_list_cold = prompts_list
prompts_list_warm = prompts_list

prompts_and_responses = set()
prompts_and_responses.update(prompts.keys())
for responses in prompts.values():
    prompts_and_responses.update(responses)


def response(text_stripped):
    if text_stripped in prompts:
        return random.choice(prompts[text_stripped])
    else:
        return random.choice(prompts_list_warm)
