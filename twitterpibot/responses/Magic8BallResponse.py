import os
import random

import re
import textwrap
from PIL import Image, ImageDraw, ImageFont

from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with

responses = ['Signs point to yes',
             'Yes',
             'Reply hazy, try again',
             'Without a doubt',
             'My sources say no',
             'As I see it, yes',
             'You may rely on it',
             'Concentrate and ask again',
             'Outlook not so good',
             'It is decidedly so',
             'Better not tell you now',
             'Very doubtful',
             'Yes - definitely',
             'It is certain',
             'Cannot predict now',
             'Most likely',
             'Ask again later',
             'My reply is no',
             'Outlook good',
             'Don\'t count on it',
             'Yes, in due time',
             'My sources say no',
             'Definitely not',
             'Yes',
             'You will have to wait',
             'I have my doubts',
             'Outlook so so',
             'Looks good to me!',
             'Who knows?',
             'Looking good!',
             'Probably',
             'Are you kidding?',
             'Go for it!',
             'Don\'t bet on it',
             'Forget about it']


def build_images():
    images_dir = "twitterpibot" + os.sep + "images" + os.sep
    template_path = images_dir + "magic8ball" + os.extsep + "png"
    print (template_path)
    template = Image.open(template_path)
    f = {}
    for r in responses:
        filename = images_dir + re.sub('[^\w]', '_', r).lower() + os.extsep + "png"
        if not os.path.isfile(filename):
            img = template.copy()
            draw = ImageDraw.Draw(img)
            wrapped = os.linesep.join(textwrap.wrap(r, width=12))
            draw.multiline_text((165, 180), wrapped, align="center")
            img.save(filename, decoder="png")
        print (r, filename)
        f[r] = filename
    return f


file_paths = build_images()


class Magic8BallResponse(Response):
    def condition(self, inbox_item):
        stream = inbox_item.is_tweet and not inbox_item.from_me and not inbox_item.is_retweet_of_my_status \
                 and inbox_item.source and "#Magic8Ball" in inbox_item.source and random.randint(0, 3) == 0

        without_mention = inbox_item.is_tweet and not inbox_item.from_me and not inbox_item.is_retweet_of_my_status \
            and ((inbox_item.sender.is_bot and random.randint(0, 3) == 0)
                or (inbox_item.sender.is_friend and random.randint(0, 1) == 0)
                or (inbox_item.sender.is_retweet_more and random.randint(0, 9) == 0)
                or random.randint(0, 99) == 0)

        return (super(Magic8BallResponse, self).condition(inbox_item) or without_mention or stream) and "?" in inbox_item.text

    def respond(self, inbox_item):
        response = random.choice(responses)
        file_path = file_paths[response]
        text = response + " #Magic8Ball"
        reply_with(inbox_item=inbox_item, text=text, file_paths=[file_path])
