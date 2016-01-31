import logging
import os
import shutil

import requests

logger = logging.getLogger(__name__)


def ensure_directory_exists(folder):
    if not os.path.exists(folder):
        logger.info("Creating " + folder)
        os.makedirs(folder)


def download_file(folder, url):
    logger.info("Downloading " + url)
    local_filename = folder + url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    logger.info("saved " + local_filename)
    return local_filename


def ensure_directory_exists_and_is_empty(folder):
    if os.path.exists(folder):
        logger.info("Removing " + folder)
        shutil.rmtree(folder, True)
    if not os.path.exists(folder):
        logger.info("Creating " + folder)
        os.makedirs(folder)


def remove_directory_and_contents(folder):
    if os.path.exists(folder):
        logger.info("Removing " + folder)
        shutil.rmtree(folder)
