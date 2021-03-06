import random

from twitterpibot.logic import jokes, phrase_generator

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

    # reactions
    "eye roll",
    "facepalm",
    "happy",
    "lol",
    "high five",
    "thumbs (up|down)",
    "wink",
    "kiss",
    "sad",

    # sound effects
    "[sad trumpet]",
    "[tumbleweed]",
    "[rimshot]",

    # Robot Noises
    "BEEP BOOP",
    "accessing",
    "biddy-biddy-biddy",

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
    # "Niiice!",
    # "what type of dog is this?",
    # "is this a cat in a hat?",
    # "wa-woo-wee-wa!",
    # "jak sie masz",

    # IT Crowd
    "have you tried turning it off and on again?",
    # "if you type 'Google' into Google, you can break the Internet",
    # "I came here to drink milk and kick ass... and I've just finished my milk",

    # Anchorman
    # "I'm very important. I have many leather-bound books and my apartment smells of rich mahogany",
    # "I immediately regret this decision",
    "I would like to extend to you an invitation to the pants party",
    "don't act like you're not impressed",
    "60 percent of the time, it works every time",
    "I'm in a glass case of emotion!",
    # "you know I don't speak Spanish",
    "I love lamp",

    # # British Stereotype
    # "jolly good show, (lads|chaps)!",
    # "impressive",
    # "splendid",
    # "I couldn't have said it better myself",
    # "and Bob's your uncle",
    # "bad (show|form)",
    # "righty-o",
    # "indeed",
    # "quite",
    # "rather",
    # "bloody hell!",
    # "cor, blimey!",
    # "chocks away!",
    # "fancy a (cuppa|pint|spot of lunch)?",
    # "Gordon Bennett!",
    # "it's a fair cop, guv(|, you've got me bang to rights)",
    # "don't get your knockers in a twist",
    # "pip pip, cheerio and all that rot",

    # # Yorkshire Stereotype
    # "blummin eck",
    # "ruddy ell",
    # "ey up",

    # # Drunk
    # "I bloody love you, you're my best mate, you are!",
    # "I could murder a kebab",

    # Looney Tunes
    "What's up doc?",

    # more reactions
    "abandon thread",
    "agree",
    "amused",
    "angry",
    "applause",
    "aroused",
    "awesome",
    "awww",
    "bfd",
    "bitch please",
    "bored",
    "burn",
    "confused",
    "cool story bro",
    "crying",
    "dancing",
    "dat ass",
    "deal with it",
    "disappointed",
    "disgusted",
    "do not want",
    "drunk",
    "embarassed",
    "eww",
    "excited",
    "eye roll",
    "facepalm",
    "finger guns",
    "fist bump",
    "flirt",
    "fml",
    "frown",
    "frustrated",
    "good job",
    "good luck",
    "goodbye",
    "gtfo",
    "hair flip",
    "happy dance",
    "hearts",
    "hello",
    "help",
    "high five",
    "hug",
    "i give up",
    "idgaf",
    "idk",
    "incredulous",
    "interested",
    "judging you",
    "kiss",
    "laughing",
    "lewd",
    "lol",
    "love",
    "mad",
    "meh",
    "mic drop",
    "middle finger",
    "no",
    "nod",
    "nom",
    "not bad",
    "oh no you didnt",
    "oh snap",
    "ok",
    "omg",
    "oops",
    "party hard",
    "please",
    "pleased",
    "popcorn",
    "proud",
    "rage",
    "rejected",
    "sad",
    "sarcastic",
    "scared",
    "serious",
    "seriously",
    "sexy",
    "shocked",
    "shrug",
    "shut up",
    "sigh",
    "sleepy",
    "slow clap",
    "smh",
    "smile",
    "sorry",
    "squee",
    "stoned",
    "success",
    "suck it",
    "suspicious",
    "table flip",
    "thank you",
    "thumbs down",
    "thumbs up",
    "ugh",
    "want",
    "what",
    "whatever",
    "win",
    "wink",
    "wow",
    "wtf",
    "yawn",
    "yes",
    "yolo",
    "you got this",

]


def get_reply():
    joke = None
    if random.randint(0, 99) == 0:
        joke = jokes.get_joke()
    if joke:
        return joke
    else:
        return phrase_generator.generate_phrase(_responses).strip()


if __name__ == "__main__":
    for i in range(100):
        print(get_reply())
