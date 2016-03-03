import logging
import os

import giphypop

from twitterpibot.logic import FileSystemHelper

logger = logging.getLogger(__name__)
folder = FileSystemHelper.root + "temp" + os.sep + "gif" + os.sep
FileSystemHelper.ensure_directory_exists(folder)
g = giphypop.Giphy()


def get_random_gif(text=None):
    gif = None
    if text:
        gif = g.translate(text)
    if not gif:
        gif = g.random_gif()

    return _download_gif(gif)


def get_gif(text):
    return _download_gif(g.translate(text))


def _download_gif(gif):
    if gif:
        return FileSystemHelper.download_file(folder=folder, url=gif.media_url)
    else:
        return None
