from unittest import TestCase

import twitterpibot.logic.gender as gender

__author__ = 'andrewtatham'

question_testcases = [
    " We want international men’s day #InternationalMensDay",
    " Why there is no #InternationalMensDay ?",
    # " #InternationalMensDay when will this be allowed?",
    " Do we need #InternationalMensDay then to even up just saying",
    " Why isn't there a men's day?",
    " There is no \"International Men's Day\" for the ",
    " when is international men’s day?",
    " Besides, when exactly is International Men’s Day?",
    " So when is men's day?",
    " Why isn't there an International Men's Day?",
    "  Is there even a international men's day? Lol",
    " Where’s the international men’s day?",
    " Is there an international men's day?"
    " Is there a international men's day?",
    " I must have missed it , but when is international men's day?",
    " Imagine the outcry if someone decided on a international mens day",
    " When is 'International mens day?'",
    " Out of interest when is International Mens Day? Asking for friends.",
    " I, for one, would like to take this opportunity to ask, WHEN IS INTERNATIONAL MENS DAY? WHAT ABOUT THE MEN? yall talk about equality smh",
    " I see Womens Day nice nice feminists now WHEN THE FUCK IS MENS DAY?",
    "Someone enlighten me pls why is there no international mens day",
    "Serious Question and please excuse my ignorance in advance - Is there such thing as International Mens Day? If so, when is it?",
    "Love the idea of international woman's day. In the interest of equality, what date is international mens day?",
    "#InternationalWomansDay where’s international mens day???!!!??? #sexist",
    "BuT wHaT aBoUt InTeRnAtIoNaL mEnS dAy??? ",
    "When its international mens day im getting a meriton with two occas to celebrate every cunt from the area is invited",
    "Imagine the backlash over a international mens day lol",
    "When’s national mens day? Girls get one, shouldn’t we?",
    "When is it national mens day ?",
    "Is there an official National Mens Day? If there isn't there needs to be one!",
    "What about international MENS day huh? Sounds like sexism if you ask me!",
    "When’s international mens day cos I’m feeling left out",
    "what is the date of international mens day?",
    "How about an #internationalmensday you sexist bitches!   ",
    "So my 9 y/o son was watching .@TuckerCarlson with me. him: Mommy what's a #InternationalWomensDay Me: A day to celebrate women Him: When's International Men's Day? Me: We don't have one Him: That's unfair, aren't men & women equal? My kid has more #CommonSense than the libs",
    "So is today National Men’s Day?",
    # "international men’s day is on april 1st",
    # "It's official We having National Mens Day tomorrow IDGAF what y'all say.",
    # "It’s Friday!!  Or like 364 days a year, it’s International Men’s Day. "

]

not_question_testcases = [
    "Every day is international mens day you ball scratching, crying, self centred hypochondriacs ",
    " its international woman's day today! Husband- so whens international mens day.... Me-........ Husband-......Me- um.. All the other 364 days of the fucking year.",
    "More Whose idea was it to to have #InternationalWomensDay on the same day as International Insecure Mens day?",
    "Intl. Mens Day is Monday the 19th of November Mr. Caller Man there. #liveline",
    "If u ask me when international mens day is, i am gonna #fart",
    "Mark your Calender, International Mens day on November 19",
    "International Men’s Day - 19th  November each year.",
    "Good morning to everyone, except for the men who asked 'When's International Men's Day?'"
    "Everyday",
    "Every day",
    "Every single day",
    "Every other day",
    "364",
    "365",
    " @Herring1967 ",
    "also known as When Is International Men's Day? Day.",
    "Male Student: when is International Men's Day?? ME: EVERY DAY IS INTERNATIONAL MENS DAY!!! Male Student: *wide eyed, point noted, backs away slowly* ME: ....my job is done here.",
    "Late to the party. @Herring1967 spent yesterday answering the question 'When is International Men's Day?' on twitter and his timeline is ",
    "Comedian Richard Herring takes it upon himself to reply to every person asking 'when is International Men's Day?' on Twitter ",
    "If everyone who asked 'when is international men's day?' yesterday, took 12 minutes to watch this video of Tony Porter talking about his Man Box, they may decide they have events to organise for Nov 19th.",
    "The effort that @Herring1967 puts into schooling the 'why isn't there an international mens day?' dorks is magnificent to behold. The fact that I interviewed him for an hour this very week without mentioning it, somewhat less so.",
    # "What do Indian men think about International Women's Day?",
    # "What do Indian men think about International Fishermen's Day?",
    "Reminders for men on international women’s day: 1 - check your privilege 2 - if you choose to speak in support of women, make sure you’re not suppressing their voices at the same time 3 - trans women are women too 4 - check the privilege of others around you marginalizing women",
    "Okay, back to International Men's Day.",
    "Today's Spin Zone with @FeitsBarstool, Should We Care About International Men's Day? ",
    "If you’re a man asking why there’s no International Men’s Day, it’s because of you "
]

all_testcases = []
all_testcases.extend(question_testcases)
all_testcases.extend(not_question_testcases)


# Hashtags
# #InternationalWomensDay
# #iwd2018
# #InternationalWomenDay2018
# internationwomensday - WTF spelling
# #InternationalMensDay

# examples


# answers
# International Men’s Day - 19th  November each year.


class TestsGender(TestCase):
    def test_is_question(self):

        for testcase in question_testcases:
            with self.subTest(testcase):
                match = gender.condition(testcase)
                if match:
                    response = gender.get_response(testcase)
                    print("response: {}".format(response))
                self.assertTrue(match)
                print()

    def test_is_answer(self):
        for testcase in not_question_testcases:
            with self.subTest(testcase):
                match = gender.condition(testcase)
                if match:
                    response = gender.get_response(testcase)
                    print("response: {}".format(response))
                self.assertFalse(match)
                print()
