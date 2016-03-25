import random
import re
from twitterpibot.logic import jokes

_responses = [

    # positive
    "nice",
    "cool",
    "hah",
    "yeah",
    "Yes",
    "Ok",
    "I like (this|that|you|those)",

    # neutral
    "[shrug]",
    "wat",
    "meh",
    "hmpfh",
    "whatever",
    "whatevs",

    # questions
    {
        "who": [
            "is this?",
            "said that?",
            "thought that was a good idea that?",
        ],
        "why": [
            "would this be?",
            "is this?",
        ],
        "what": [
            "is (this|that)?",
            "do you (think|say|know|feel) about this?"
        ],
        "when": [
            "did (this|that) happen?",
            "do you want (it|this) by?",
            "will we learn?",
        ],
        "is": [
            "(that|this) a good idea?",
            "there a better way to (say|put|express|do|achieve) (this|that)?"
        ],
    },

    # negative
    "No",
    "Nah",
    "I (didn't|don't) think so",

    # indecisive
    "I'm not sure really",
    "I don't know",

    # sound effects
    "[sad trumpet]",
    "[tumbleweed]",
    "[rimshot]",

    # Robot Noises
    "BEEP BOOP",
    "accessing",
    "biddy-biddy-biddy"

    # father ted
    "that would be an ecumenical matter",
    "down with this sort of thing! Careful now.",
    "is there anything to be said for another mass?",
    "that money was just resting in my account!",
    "as I said last time, it won't happen again",
    # You'll have some tea...
    # are you sure you don't want any?
    # Aw go on,
    # you'll have some.
    # Go on
    # go on go on go on go on go on go on go on GO ON!

    # Borat
    "Niiice!",
    "what type of dog is this?",
    "is this a cat in a hat?",
    "wa-woo-wee-wa!",
    "jak sie masz",

    # IT Crowd
    "have you tried turning it off and on again?",
    "if you type 'Google' into Google, you can break the Internet",
    "I came here to drink milk and kick ass... and I've just finished my milk",

    # Anchorman
    "I'm very important. I have many leather-bound books and my apartment smells of rich mahogany",
    "I immediately regret this decision",
    "I would like to extend to you an invitation to the pants party",
    "don't act like you're not impressed",
    "60 percent of the time, it works every time",
    "I'm in a glass case of emotion!",
    "you know I don't speak Spanish",
    "I love lamp",

    # British Stereotype
    "jolly good show, (lads|chaps)!",
    "impressive",
    "splendid",
    "I couldn't have said it better myself",
    "and Bob's your uncle",
    "bad (show|form)",
    "righty-o",
    "indeed",
    "quite",
    "rather",
    "bloody hell!",
    "cor, blimey!",
    "chocks away!",
    "fancy a (cuppa|pint|spot of lunch)?",
    "Gordon Bennett!",
    "it's a fair cop, guv(|, you've got me bang to rights)",
    "don't get your knockers in a twist",
    "pip pip, cheerio and all that rot",

    # Yorkshire Stereotype
    "blummin eck",
    "ruddy ell",
    "ey up",

    # Drunk
    "I bloody love you, you're my best mate, you are!",
    "I could murder a kebab",

    # Looney Tunes
    "What's up doc?",

]

choice_rx = re.compile("\(.*\)")


def _recurse(text, response):
    if isinstance(response, list):
        return _recurse(text, random.choice(response))
    elif isinstance(response, dict):
        key = random.choice(response)
        text += " " + key
        return _recurse(text, random.choice(response[key]))
    else:
        # string
        matches = choice_rx.findall(response)
        if matches:

            for match in matches:
                choices = match[1:-1].split("|")
                choice = random.choice(choices)
                response = response.replace(match, choice)

        text += " " + response
        return text


def get_reply():
    if random.randint(0, 9) == 0:
        return jokes.get_joke()
    return _recurse(text="", response=_responses)


if __name__ == "__main__":
    for i in range(100):
        print(get_reply())
