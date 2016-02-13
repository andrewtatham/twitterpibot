from itertools import cycle
import random

ep1 = "https://youtu.be/qjOZtWZ56lc"
ep2 = "https://youtu.be/zJDu5D_IXbc"
number_board_game = "https://youtu.be/swV3E3HPQC4"
history_of_numberwang = "https://youtu.be/-r6NY4Kl8Ms"
numberwang_code = "https://youtu.be/yHxHQ00uvcc"
numberwang_meeting = "https://youtu.be/oVItKzP6IBY"
wordwang = "https://youtu.be/gCHktd1VrGY"
numberwang_live = "https://youtu.be/gq3wWpGJymM"






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


def play_numberwang_round(contestants, round_type):
    c = cycle(contestants)
    prev_answers = []
    for n in range(random.randint(1, 10)):
        contestant = next(c)

        answer = numberwang(prev_answers)
        print(contestant + ": " + str(answer))
        prev_answers.append(answer)
        if random.randint(0, 49) == 0:
            print ("[KLAXON] Thats the " + round_type + " bonus. Triple " + round_type + " to " + contestant + "!")
            break

    print("That's " + round_type + "!")
    if round_type == "Numberwang":
        for c in contestants:
            print(c + " you are " + random.choice(["ahead", "behind"]) + " with " + str(random.randint(-10, 100)))
    elif round_type == "Wanganum":
        random.shuffle(contestants)
        winner = contestants[len(contestants) - 1]
        for c in contestants:
            if c == winner:
                print(c + " you are todays Numberwang!")
            else:
                print("Bad luck " + c + " you've been Wanganumed!")


def play_numberwang(contestants):
    intro = "Now you can play the maths quiz that simply everyone is talking about!"
    print(intro)

    contestant_locations = [
        "Somerset",
        ["Northampton", "Southampton"]
    ]

    location = random.choice(contestant_locations)
    if isinstance(location, basestring):
        locations = None
    else:
        locations = cycle(location)
        location = None

    intro2 = "Our contestants today are "
    first = True
    for contestant in contestants:
        if not first:
            intro2 += " and "
        intro2 += contestant
        if locations:
            location = next(locations)
            if first:
                intro2 += " who is from " + location
            else:
                intro2 += " who is also from " + location
        elif location:
            intro2 += " who is from " + location
        first = False
    print(intro2)

    question = random.choice(["Any funny stories?", "Any hobbies?", "Any pets?", "Ever killed a man?"])
    contestant_replies = ["Yes", "No"]
    random.shuffle(contestant_replies)
    contestant_replies = cycle(contestant_replies)
    for contestant in contestants:
        print (contestant + " " + question)
        print (contestant + ": " + next(contestant_replies))
        print (random.choice(["Good", "Great", "Right"]))

    print ("Let's play Numberwang!")

    for round in range(random.randint(2,5)):
        play_numberwang_round(contestants, "Numberwang")

    # TODO maths board, imaginary numbers, numberbounce, all same digits (4, 44, 444, 4.444)

    print ("Everthing hinges on this final round. Yes its time for Wanganum.")
    print ("Let's rotate the board!")
    play_numberwang_round(contestants, "Wanganum")
    print("That's all from Numberwang! Until tommorrows edition: Stay Numberwang!")


contestants_list = ["@andrewtathampi", "@andrewtathampi2"]

play_numberwang(contestants_list)
