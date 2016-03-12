import os
import random
import re
import textwrap
import logging

# noinspection PyPackageRequirements
from PIL import Image, ImageDraw
from twitterpibot.logic import fsh

logger = logging.getLogger(__name__)

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


def _build_image(r):
    filename = images_dir + re.sub('[^\w]', '_', r).lower() + os.extsep + "png"
    if not os.path.isfile(filename):
        logger.info(r + " " + filename)
        img = template.copy()
        draw = ImageDraw.Draw(img)
        wrapped = os.linesep.join(textwrap.wrap(r, width=12))
        draw.multiline_text((165, 180), wrapped, align="center")
        img.save(filename, decoder="png")
    return filename


template_path = "twitterpibot" + os.sep + "images" + os.sep + "magic8ball" + os.extsep + "png"
template = Image.open(template_path)
images_dir = "temp" + os.sep + "images" + os.sep + "magic8ball" + os.sep
fsh.ensure_directory_exists(images_dir)
file_paths = {}
for r in responses:
    file_paths[r] = _build_image(r)


def get_response():
    return random.choice(responses)


def get_image(response):
    if response not in file_paths:
        logger.info("building image for %s", response)
        file_paths[response] = _build_image(response)
    return file_paths[response]
