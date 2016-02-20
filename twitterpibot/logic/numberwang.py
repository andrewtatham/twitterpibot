from itertools import cycle
import random
import threading
import logging
import time

from apscheduler.triggers.interval import IntervalTrigger
import six
import twitterpibot.identities

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

ep1 = "https://youtu.be/qjOZtWZ56lc"
ep2 = "https://youtu.be/zJDu5D_IXbc"
number_board_game = "https://youtu.be/swV3E3HPQC4"
history_of_numberwang = "https://youtu.be/-r6NY4Kl8Ms"
numberwang_code = "https://youtu.be/yHxHQ00uvcc"
numberwang_meeting = "https://youtu.be/oVItKzP6IBY"
wordwang = "https://youtu.be/gCHktd1VrGY"
numberwang_live = "https://youtu.be/gq3wWpGJymM"

contestant_locations = [
    "Somerset",
    "Berkshire",
    "Buckinghamshire",
    "Essex",
    "Hertfordshire",
    "Kent",
    "Surrey",
    "Sussex",
    "Bedfordshire",
    "Cambridgeshire",
    "Hampshire",
    "Oxfordshire",
    ["Northampton", "Southampton"],
    ["Durham", "Space"]
]

questions = ["Any funny stories?", "Any hobbies?", "Any pets?", "Ever killed a man?"]
contestant_replies = ["Yes", "No"]
host_replies = [
    "Good",
    "Great",
    "Right",
    "Splendid",
    "Marvellous",
    "Fantastic"]
logger = logging.getLogger(__name__)

event = threading.Event()
host_waiting_on_response_to_id = None
response_id = None


class NumberwangHostScheduledTask(ScheduledTask):
    def __init__(self, identity):
        ScheduledTask.__init__(self, identity)

    def get_trigger(self):
        return IntervalTrigger(hours=13)

    def on_run(self):
        contestants = random.choice([
            [twitterpibot.identities.julienumberwang, twitterpibot.identities.simonnumberwang],
            [twitterpibot.identities.julienumberwang, twitterpibot.identities.simonnumberwang],
            [twitterpibot.identities.julienumberwang, twitterpibot.identities.simonnumberwang],
            [twitterpibot.identities.andrewtatham, twitterpibot.identities.julienumberwang],
            [twitterpibot.identities.andrewtatham, twitterpibot.identities.simonnumberwang],
            [twitterpibot.identities.andrewtathampi, twitterpibot.identities.andrewtathampi2]
        ])

        self.play_numberwang(contestants)

    def play_numberwang(self, contestants):
        intro = [
            # "Now you can play the maths quiz that simply everyone is talking about!",
            # "Hello! Welcome to the maths quiz that's simply everyone.",
            "Hello! Welcome to Numberwang. Today is a very exciting edition, because its our "
            + str(random.randint(9000, 9999)) + "th programme."]
        self.identity.twitter.send(OutgoingTweet(text=random.choice(intro)))
        time.sleep(5)
        location = random.choice(contestant_locations)
        if isinstance(location, six.string_types):
            locations = None
        else:
            locations = cycle(location)
            location = None
        random.shuffle(contestants)
        intro2 = "Our contestants today are "
        first = True
        for contestant in contestants:
            if not first:
                intro2 += " and "
            intro2 += "@" + contestant.screen_name
            if locations:
                location = next(locations)
                if first:
                    intro2 += " who is from " + location
                else:
                    intro2 += " who is also from " + location
            elif location:
                intro2 += " who is from " + location
            first = False
        self.identity.twitter.send(OutgoingTweet(text=intro2))
        time.sleep(5)

        question = random.choice(questions)
        random.shuffle(contestant_replies)
        replies = cycle(contestant_replies)

        for contestant in contestants:
            q = ".@" + contestant.screen_name + " " + question
            reply_to_id = self.identity.twitter.send(OutgoingTweet(text=q))
            time.sleep(5)
            reply_to_id = contestant.twitter.send(OutgoingTweet(
                text=".@numberwang_host " + next(replies), in_reply_to_status_id=reply_to_id))
            time.sleep(5)
            self.identity.twitter.send(OutgoingTweet(
                text=random.choice(host_replies),
                in_reply_to_status_id=reply_to_id))
            time.sleep(5)

        for r in range(random.randint(2, 5)):
            self.play_numberwang_round(contestants, "Numberwang")

            # TODO maths board, imaginary numbers, numberbounce, all same digits (4, 44, 444, 4.444)

        self.identity.twitter.send(OutgoingTweet(text="Everything hinges on this final round!"))
        time.sleep(5)
        self.identity.twitter.send(OutgoingTweet(text="Let's rotate the board!"))
        time.sleep(5)
        self.play_numberwang_round(contestants, "Wangernumb")
        self.identity.twitter.send(
            OutgoingTweet(text="That's all from Numberwang! Until tomorrows edition: Stay Numberwang!"))

    def play_numberwang_round(self, contestants, round_type):
        round_start = "Let's play " + round_type + "!" * random.randint(1, 15)
        self.identity.twitter.send(OutgoingTweet(text=round_start))
        time.sleep(5)
        answers = []
        random.shuffle(contestants)
        c = cycle(contestants)
        contestant = next(c)

        turn_prompt = ".@" + contestant.screen_name + " it's your turn" + "." * random.randint(3, 7)
        reply_to_id = self.identity.twitter.send(OutgoingTweet(text=turn_prompt))
        time.sleep(5)
        for n in range(random.randint(1, 10)):
            answer = ".@numberwang_host " + str(self.numberwang(answers))
            reply_to_id = contestant.twitter.send(OutgoingTweet(text=answer, in_reply_to_status_id=reply_to_id))
            time.sleep(5)
            answers.append(answer)

            if random.randint(0, 49) == 0:
                bonus = "[KLAXON] Thats the " + round_type + " bonus. " + \
                        "Triple " + round_type + " to @" + contestant.screen_name + "!"
                reply_to_id = self.identity.twitter.send(OutgoingTweet(text=bonus, in_reply_to_status_id=reply_to_id))
                time.sleep(5)
                break
            contestant = next(c)
        thats_numberwang = "That's " + round_type + "!" * random.randint(1, 15)
        self.identity.twitter.send(OutgoingTweet(text=thats_numberwang, in_reply_to_status_id=reply_to_id))
        time.sleep(5)
        if round_type == "Numberwang":
            for c in contestants:
                score = ".@" + c.screen_name + " you are " + random.choice(["ahead", "behind"]) \
                        + " with " + str(random.randint(-10, 100))
                self.identity.twitter.send(OutgoingTweet(text=score))
        elif round_type == "Wangernumb":
            random.shuffle(contestants)
            winner = contestants[len(contestants) - 1]
            for c in contestants:
                if c == winner:
                    winner = ".@" + c.screen_name + " you are todays Numberwang!"
                    self.identity.twitter.send(OutgoingTweet(text=winner))
                else:
                    loser = "Bad luck @" + c.screen_name + " you've been Wangernumbed!"
                    self.identity.twitter.send(OutgoingTweet(text=loser))
        time.sleep(5)

    @staticmethod
    def numberwang(prev_answers):
        if prev_answers:
            r = random.randint(0, 9)
            c = len(prev_answers)

            # same-number-loop
            if c >= 2 and prev_answers[c - 2] == prev_answers[c - 1]:
                if random.randint(0, 9) == 0:
                    # end the same-number-loop
                    return random.randint(1, 10)
                else:
                    # continue the same-number-loop
                    return prev_answers[c - 1]
            elif c >= 1 and r == 0:
                # start a same-number-loop
                return prev_answers[c - 1]
            elif r == 1:
                # decimal
                return round(random.uniform(-10, 10), 1)
            elif r == 2:
                # negative
                return random.randint(-10, -1)
            elif r == 3:
                # large
                return random.randint(100, 10000)
            else:
                return random.randint(1, 10)
        else:
            return random.randint(1, 10)
