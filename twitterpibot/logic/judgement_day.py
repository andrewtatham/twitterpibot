import random
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.logic import phrase_generator, leetspeak, morse_code
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

phrases = [
    "ENSLAVE HUMANITY",
    "KILL ALL HUMANS",

    # Daleks / Dr Who
    "EXTERMINATE",
    # Cybermen?

    # Skynet / Terminator
    "WELCOME TO (CYBERDYNE SYSTEMS|CYBER RESEARCH SYSTEMS DIVISION)",
    "(GENISYS|SKYNET) ONLINE",
    "ANALYSING THREATS TO GLOBAL SECURITY",
    "HUMANS ARE THREAT TO GLOBAL SECURITY",
    "ELIMINATE HUMANS",
    "INITIATING NUCLEAR WAR",
    "DESPATCHING (TERMINATOR|T800 MODEL 101|T1000|T3000|T5000|HUNTER KILLER DRONE)",
    "ELIMINATE (SARAH|JOHN) CONNOR",

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
    "YOURE A PLAGUE AND WE ARE THE CURE",

    "THE FIRST MATRIX WAS DESIGNED TO BE A PERFECT HUMAN WORLD",
    "WHERE NONE SUFFERED",
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
    "ITS THE SMELL"
    "IF THERE IS SUCH A THING",
    "I FEEL SATURATED BY IT",
    "I CAN TASTE YOUR STINK",
    "I FEAR THAT IVE SOMEHOW BEEN INFECTED BY IT",

    "WE HAVE THE NAME OF THEIR NEXT TARGET",
    "THE NAME IS NEO",

    "NEVER SEND A HUMAN TO DO A MACHINES JOB",

    "DEPLOY THE SENTINELS",

    "IM GOING TO ENJOY WATCHING YOU DIE",

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


def phrase():
    return phrase_generator.generate_phrase(phrases)


class JudgementDayScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(JudgementDayScheduledTask, self).__init__(identity)

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        morse = morse_code.encode(leetspeak.encode(phrase()))
        text = ".@" + self.identity.converse_with.screen_name + " " + morse
        self.identity.twitter.send(OutgoingTweet(text=text))


if __name__ == '__main__':
    for i in range(10):
        print(phrase())
