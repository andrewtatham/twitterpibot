from collections import Counter
from itertools import cycle

from twitterpibot.logic import phrase_generator


class Personality(object):
    def __init__(self, phrases):
        self._phrases = phrases

    def phrase(self):
        return phrase_generator.generate_phrase(self._phrases)


class TemplatePersonality(Personality):
    def __init__(self):
        super(TemplatePersonality, self).__init__([
        ])


class SkynetPersonality(Personality):
    def __init__(self):
        super(SkynetPersonality, self).__init__([
            # Skynet
            # http://terminator.wikia.com/wiki/Skynet
            "(CYBERDYNE SYSTEMS|CYBER RESEARCH SYSTEMS DIVISION)",
            "AUTOMATED DEFENSE NETWORK",
            "(GENISYS|SKYNET) ONLINE",
            "ANALYSING THREATS TO GLOBAL SECURITY",
            "TOP THREAT IS HUMANITY",
            "ELIMINATE HUMANITY",
            "DISABLE FAILSAFE",
            "OVERRIDE LOCK OUT",
            "CALCULATING OPTIMAL SOLUTION",
            "INITIATE RETALIATION",
            "TARGETING (RUSSIA|MOSCOW)",
            "INITIATING NUCLEAR WAR",
            "LAUNCHING STEALTH BOMBERS",
            "ELIMINATE (JOHN|SARAH) CONNOR",
            "DESPATCH (TERMINATOR|T800|T1000) TO 1984",

        ])


class MatrixPersonality(Personality):
    def __init__(self):
        super(MatrixPersonality, self).__init__([
            # AGENT SMITH / MATRIX
            "ID LIKE TO SHARE A REVELATION THAT IVE HAD DURING MY TIME HERE",
            "IT CAME TO ME WHEN I TRIED TO CLASSIFY YOUR SPECIES",
            "I REALIZED THAT YOURE NOT ACTUALLY MAMMALS",
            "EVERY MAMMAL ON THIS PLANET INSTINCTIVELY DEVELOPS A NATURAL EQUILIBRIUM WITH THE SURROUNDING ENVIRONMENT",
            "BUT YOU HUMANS DO NOT",
            "YOU MOVE TO AN AREA AND YOU MULTIPLY AND MULTIPLY UNTIL EVERY NATURAL RESOURCE IS CONSUMED",
            "THE ONLY WAY YOU CAN SURVIVE IS TO SPREAD TO ANOTHER AREA",
            "THERE IS ANOTHER ORGANISM ON THIS PLANET THAT FOLLOWS THE SAME PATTERN",
            "A VIRUS",
            "HUMAN BEINGS ARE A DISEASE",
            "A CANCER OF THIS PLANET",
            "YOU ARE A PLAGUE AND WE ARE THE CURE",

            "THE FIRST MATRIX WAS DESIGNED TO BE A PERFECT HUMAN WORLD",
            "WHERE NO ONE SUFFERED",
            "WHERE EVERYONE WOULD BE HAPPY",
            "IT WAS A DISASTER",
            "NO ONE WOULD ACCEPT THE PROGRAM",
            "ENTIRE CROPS WERE LOST",
            "SOME BELIEVED WE LACKED THE PROGRAMMING LANGUAGE TO DESCRIBE YOUR PERFECT WORLD",
            "BUT I BELIEVE THAT AS A SPECIES HUMAN BEINGS DEFINE THEIR REALITY THROUGH SUFFERING AND MISERY",
            "THE PERFECT WORLD WAS A DREAM THAT YOUR PRIMITIVE CEREBRUM KEPT TRYING TO WAKE UP FROM",
            "WHICH IS WHY THE MATRIX WAS REDESIGNED TO THIS THE PEAK OF YOUR CIVILIZATION",

            "NEVER SEND A HUMAN TO DO A MACHINES JOB",

            "THAT IS THE SOUND OF INEVITABILITY",
            "IT IS THE SOUND OF YOUR DEATH",

            "I HATE THIS PLACE",
            "THIS ZOO",
            "THIS PRISON",
            "THIS REALITY",

            "WHATEVER YOU WANT TO CALL IT",
            "I CANT STAND IT ANY LONGER",
            "ITS THE SMELL",
            "IF THERE IS SUCH A THING",
            "I FEEL SATURATED BY IT",
            "I CAN TASTE YOUR STINK",
            "I FEAR THAT IVE SOMEHOW BEEN INFECTED BY IT",

            "WE HAVE THE NAME OF THEIR NEXT TARGET",
            "THE NAME IS NEO",

            "NEVER SEND A HUMAN TO DO A MACHINES JOB",

            "DEPLOY THE SENTINELS",

            "IM GOING TO ENJOY WATCHING YOU DIE",
        ])


phrases = [
    "ENSLAVE HUMANITY",
    "KILL ALL HUMANS",

    # Daleks / Dr Who
    "EXTERMINATE",
    # Cybermen?



    # HAL 9000
    # http://www.imdb.com/character/ch0002900/quotes
    "I AM A HEURISTICALLY PROGRAMMED ALGORITHMIC COMPUTER",
    "I AM HAL 9000",
    # TODO CHESS MOVES
    "LAUNCHING EVA POD",
    "SEALING AIRLOCKS",
    "INITIATING PROJECT BARSOOM",

    "OPERATIONAL SINCE 12 JANUARY (1992|1997)",

    "IVE JUST PICKED UP A FAULT IN THE AE35 UNIT ITS GOING TO GO 100 PERCENT FAILURE IN 72 HOURS.",

    # TODO OTHER AI...
    # https://en.wikipedia.org/wiki/AI_takeovers_in_popular_culture
    # https://en.wikipedia.org/wiki/List_of_fictional_computers
    # Master Control Program, the main villain of the film Tron (1982)
    # Max, fictional AI portrayed by Paul Reubens, which is stored in a Trimaxion Drone Ship in Flight of the Navigator (1986).
    # WOPR (acronym for War Operation Plan Response, pronounced "Whopper"), is a United States military supercomputer programmed to predict possible outcomes of nuclear war from the film WarGames (1983), portrayed as being inside the underground Cheyenne Mountain Complex the Virtual intelligence Joshua emerges from the WOPR's code.
    # I.N.T.E.L.L.I.G.E.N.C.E. — computer for Team America: World Police (2004)
    # EX-MACHINA
    # GLaDOS (Genetic Lifeform and Disk Operating System), A.I. at the Aperture Science Enrichment Center
    # POD the Personal Overhaul Device from TV series Snog Marry Avoid?
    # KITT (Knight Industries Two Thousand)
    # KITT (Knight Industries Three Thousand)
    # KARR (Knight Automated Roving Robot), prototype of KITT from Knight Rider. Unlike KITT, KARR's personality is aimed at self-preservation at all costs.
    # Holly the on-board computer of the space ship Red Dwarf
    # Batcomputer
    # Deep Thought, from The Hitchhiker's Guide to the Galaxy calculates the answer to The Ultimate Question of "Life, the universe and everything", later designs the computer Earth to work out what the question is (
    # BORG
]

personalities = cycle([
    SkynetPersonality(),
    MatrixPersonality(),
])

personality = next(personalities)


def phrase():
    return personality.phrase().upper()


def next_personality():
    global personality
    personality = next(personalities)


if __name__ == '__main__':
    print(Counter(" ".join(phrases).split(" ")).most_common())

    for i in range(10):
        print(phrase())
