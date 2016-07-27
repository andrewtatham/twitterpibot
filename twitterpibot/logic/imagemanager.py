import logging
import os
import pprint
import random

from twitterpibot.logic import googlehelper, fsh, giphyhelper

logger = logging.getLogger(__name__)
folder = fsh.root + "temp" + os.sep + "images" + os.sep + "imagemanager" + os.sep
ed_balls = []
ed_balls_folder = fsh.root + "twitterpibot" + os.sep + "images" + os.sep + "edballs" + os.sep


# todo empty dir / manage files and cache

def get_image(topics):
    logger.info("get_image: {}".format(topics))
    topic = random.choice(topics)
    images = googlehelper.get_search_images(topic, 5)
    logger.debug("get_image: {}".format(pprint.pformat(images)))
    image_url = random.choice(images)
    file_path = fsh.download_file(folder, image_url, topic + ".jpg")
    return file_path


def get_reply_image(screen_name, text):
    logger.info("get_reply_image: {} {}".format(screen_name, text))
    image_url = giphyhelper.get_random_gif(text=text)
    logger.info(image_url)
    ext = fsh.get_url_extension(image_url)
    file_path = fsh.download_file(folder, image_url, screen_name + "_" + text + ext)
    return file_path


def get_gif(screen_name, text):
    logger.info("get_gif: {} {}".format(screen_name, text))
    image_url = giphyhelper.get_gif(text=text)
    logger.info(image_url)
    ext = fsh.get_url_extension(image_url)
    file_path = fsh.download_file(folder, image_url, screen_name + "_" + text + ext)
    return file_path


def get_ed_balls_image():
    global ed_balls
    if not ed_balls:
        ed_balls = list(fsh.get_files_in_folder(ed_balls_folder))
        random.shuffle(ed_balls)
    return ed_balls.pop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # print(get_image(["eggs", "egg"]))
    # print(get_reply_image("test", "blah"))
    # print(get_gif("test", "wat"))
    for _ in range(20):
        print(get_ed_balls_image())


def download_images(image_urls):
    file_paths = []
    for image_url in image_urls:
        if image_url:
            try:
                file_path = fsh.download_file(folder, image_url)
                if file_path:
                    file_paths.append(file_path)
            except Exception as ex:
                logger.error(ex)
    return file_paths
