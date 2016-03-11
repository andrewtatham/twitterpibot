import csv
import logging
import shutil
import os
import sys

import six
import requests

try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    input = raw_input
except NameError:
    pass

import pickle

logger = logging.getLogger(__name__)


def ensure_directory_exists(folder):
    if not os.path.exists(folder):
        logger.info("Creating " + folder)
        os.makedirs(folder)


def download_file(folder, url, file_name=None):
    logger.info("Downloading " + url)
    ensure_directory_exists(folder)
    if file_name:
        local_filename = folder + file_name
    else:
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


valid_extensions = {".jpg", ".jpeg", ".gif", ".png"}


def check_extension(url):
    ext = get_url_extension(url).lower()
    return ext in valid_extensions


def get_url_extension(url):
    path = six.moves.urllib.parse.urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext


def delete_files(files_list):
    if files_list:
        for file in files_list:
            if os.path.exists(file):
                logger.info("Removing " + file)
                os.remove(file)


def bytes_from_file(file_path, chunk_size):
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


def get_key(key_name):
    return _get("key", key_name)


def get_username(key_name):
    return _get("username", key_name)


def get_password(key_name):
    return _get("password", key_name)


def _get(key_type, key_name):
    keys_dir = get_root() + "temp" + os.sep + key_type + "s" + os.sep + str(sys.version_info[0]) + os.sep
    ensure_directory_exists(keys_dir)
    key_path = keys_dir + key_name + ".pkl"
    exists = os.path.isfile(key_path)
    if exists:
        key = pickle.load(open(key_path, "rb"))
    else:
        key = input("Enter your " + key_type + " for " + key_name + ": ")
        pickle.dump(key, open(key_path, "wb"))
    return key


def get_root():
    path = ""
    while not os.path.exists(path + "mainscript.py"):
        path += "../"
    return path


root = get_root()


def exists(csv_path):
    return bool(os.path.isfile(csv_path))


def parse_csv(csv_path):
    with open(csv_path, 'r') as csvfile:
        data_csv = csv.reader(csvfile)
        data_dict = {}
        for row in data_csv:
            logger.info(row)
            data_dict[row[0]] = row
        return data_dict
