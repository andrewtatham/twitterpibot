import logging
import os

import giphypop

from twitterpibot.logic import FileSystemHelper

logger = logging.getLogger(__name__)
folder = "temp" + os.sep + "gif" + os.sep
FileSystemHelper.ensure_directory_exists(folder)
g = giphypop.Giphy()


def get_random_gif(text=None):
    gif = None
    if text:
        gif = g.translate(text)
    if not gif:
        gif = g.random_gif()
    path = FileSystemHelper.download_file(gif.media_url)
    return path
