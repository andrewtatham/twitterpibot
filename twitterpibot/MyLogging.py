import logging
from logging import handlers
import os

rootlogger = logging.getLogger("")
rootlogger.setLevel(logging.DEBUG)

dir = "temp" + os.sep + "log" + os.sep

if not os.path.exists(dir):
    os.makedirs(dir)


file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

debug_file_log = handlers.RotatingFileHandler(dir + "twitter_debug.log", maxBytes=4 * 1024 * 1024, backupCount=2)
debug_file_log.setLevel(logging.DEBUG)
debug_file_log.setFormatter(file_formatter)
rootlogger.addHandler(debug_file_log)

warning_file_log = handlers.RotatingFileHandler(dir + "twitter_warning.log", maxBytes=4 * 1024 * 1024, backupCount=2)
warning_file_log.setLevel(logging.WARNING)
warning_file_log.setFormatter(file_formatter)
rootlogger.addHandler(warning_file_log)

error_file_log = handlers.RotatingFileHandler(dir + "twitter_error.log", maxBytes=4 * 1024 * 1024, backupCount=2)
error_file_log.setLevel(logging.ERROR)
error_file_log.setFormatter(file_formatter)
rootlogger.addHandler(error_file_log)


# create console handler with a higher log level

console_formatter = logging.Formatter('%(asctime)s [%(name)s] %(message)s')
console_log = logging.StreamHandler()
console_log.setLevel(logging.INFO)
console_log.setFormatter(console_formatter)
rootlogger.addHandler(console_log)


def init():
    pass
