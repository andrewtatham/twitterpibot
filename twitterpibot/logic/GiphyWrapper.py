import logging
import os

import requests
import giphypop

logger = logging.getLogger(__name__)
folder = "temp" + os.sep + "gif" + os.sep

if not os.path.exists(folder):
    logger.info("Creating " + folder)
    os.makedirs(folder)


def download_file(url):
    local_filename = folder + url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return local_filename


g = giphypop.Giphy()


def get_random_gif(text=None):
    gif = None
    if text:
        gif = g.translate(text)
    if not gif:
        gif = g.random_gif()
    path = download_file(gif.media_url)
    return gif.media_url, path
