import random
import re

_responses = [

    # positive
    "Nice",
    "Cool",
    "Hah",
    "Yeah",
    "Indeed",
    "Yes",
    "Ok",
    "I like (this|that|you|those)",

    # neutral
    "[Shrug]",
    "Wat",
    "Meh",
    "Hmpfh",
    "Whatever",
    "Whatevs",

    # questions
    {"Who": [
        "is this?",
        "said that?",
        "thought that was a good idea that?",
    ]},
    {"Why": [
        "would this be?",
        "is this?",

    ]},
    {"What": ["is this?", "is that?"]},
    {"When": ["did this happen?"]},

    {"is": [
        "(that|this) a good idea?",
        "there a better way to (say|put|express|do|achieve) (this|that)?"
    ]},

    # negative
    "No",
    "Nah",
    "I dont think so"

    # indecisive
    "I'm not sure really",
    "I don't know",

    # Robot Noises
    "BEEP BOOP",

    # father ted
    "That would be an ecumenical matter",
    "Down with this sort of thing! Careful now.",
    "Is there anything to be said for another mass?",
    "That money was just resting in my account!",
    "as I said last time, it won't happen again",
    # You'll have some tea...  are you sure you don't want any?  Aw go on,
    # you'll have some.  Go on go on go on go on go on go on go on go on GO
    # ON!

    # Borat
    "Niiice!",
    "What type of dog is this?",
    "Is this a cat in a hat?",
    "Wa-woo-wee-wa!",
    "Jak sie masz",

    # IT Crowd
    "Have you tried turning it off and on again?",
    "If you type 'Google' into Google, you can break the Internet",
    "I came here to drink milk and kick ass... and I've just finished my milk",

    # Anchorman
    "I'm very important. I have many leather-bound books and my apartment smells of rich mahogany",
    "I immediately regret this decision",
    "I would like to extend to you an invitation to the pants party",
    "Don't act like you're not impressed",
    "60 percent of the time, it works every time",
    "I'm in a glass case of emotion!",
    "You know I don't speak Spanish",
    "I love lamp",

    # British Stereotype
    "jolly good show, (lads|chaps)!",
    "impressive",
    "splendid",
    "I couldn't have said it better myself",
    "and Bob's your uncle",
    "bad (show|form)",
    "righty-o",
    "quite",
    "rather",
    "Bloody hell!",
    "Cor, blimey!",
    "Chocks away!",
    "Fancy a (cuppa|pint)?",
    "Gordon Bennett!",
    "It's a fair cop, guv(|, you've got me bang to rights)",
    "Don't get your knockers in a twist",
    "Pip pip, cheerio and all that rot"

    # Yorkshire Stereotype
    "Blummin eck",
    "Ruddy ell",
    "Ey up",

    # Drunk
    "I bloody love you, you're my best mate, you are!",
    "I could murder a kebab",
    
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
    return _recurse(text="", response=_responses)


if __name__ == "__main__":
    for i in range(100):
        print(get_reply())
