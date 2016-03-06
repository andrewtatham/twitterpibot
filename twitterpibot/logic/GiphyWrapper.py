import logging
import os

import giphypop

from twitterpibot.logic import FileSystemHelper

logger = logging.getLogger(__name__)

g = None


def _init(screen_name):
    global g
    if not g:
        g = giphypop.Giphy()

    folder = FileSystemHelper.root + "temp" + os.sep + "gif" + os.sep + screen_name + os.sep
    FileSystemHelper.ensure_directory_exists(folder)
    return folder


def get_random_gif(screen_name, text=None):
    folder = _init(screen_name)
    gif = None
    if text:
        gif = g.translate(text)
    if not gif:
        gif = g.random_gif()

    return _download_gif(folder, gif)


def get_gif(screen_name, text):
    folder = _init(screen_name)
    return _download_gif(folder, g.translate(text))


def _download_gif(folder, gif):
    if gif:
        return FileSystemHelper.download_file(folder=folder, url=gif.media_url)
    else:
        return None
