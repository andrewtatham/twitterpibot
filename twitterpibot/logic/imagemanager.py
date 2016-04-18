import logging
import os
import random

from twitterpibot.logic import googlehelper, fsh, giphyhelper

__author__ = 'andrewtatham'
folder = fsh.root + "temp" + os.sep + "images" + os.sep + "imagemanager" + os.sep

logger = logging.getLogger(__name__)


# todo empty dir / manage files and cache

def get_image(topics):
    logger.info("get_image: {}".format(topics))
    topic = random.choice(topics)
    images = googlehelper.get_search_images(topic, 5)
    image_url = random.choice(images)
    file_path = fsh.download_file(folder, image_url, topic + ".jpg")
    return file_path


def get_reply_image(screen_name, text):
    logger.info("get_reply_image: {} {}".format(screen_name, text))
    image_url = giphyhelper.get_random_gif(text=text)
    ext = fsh.get_url_extension(image_url)
    file_path = fsh.download_file(folder, image_url, screen_name + "_" + text + ext)
    return file_path


def get_gif(screen_name, text):
    logger.info("get_gif: {} {}".format(screen_name, text))
    image_url = giphyhelper.get_gif(text=text)
    ext = fsh.get_url_extension(image_url)
    file_path = fsh.download_file(folder, image_url, screen_name + "_" + text + ext)
    return file_path


if __name__ == '__main__':
    print(get_image(["eggs", "egg"]))
    print(get_reply_image("test", "blah"))
    print(get_gif("test", "wat"))
