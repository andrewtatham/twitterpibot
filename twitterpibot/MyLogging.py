import logging
from logging import handlers
import os

from twitterpibot.logic import FileSystemHelper

root_logger = logging.getLogger("")
root_logger.setLevel(logging.INFO)

log_dir = FileSystemHelper.root + "temp" + os.sep + "log" + os.sep

FileSystemHelper.ensure_directory_exists(log_dir)

file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

debug_file_log = handlers.RotatingFileHandler(log_dir + "twitter_debug.log", maxBytes=4 * 1024 * 1024, backupCount=2)
debug_file_log.setLevel(logging.DEBUG)
debug_file_log.setFormatter(file_formatter)
root_logger.addHandler(debug_file_log)

warning_file_log = handlers.RotatingFileHandler(log_dir + "twitter_warning.log", maxBytes=4 * 1024 * 1024,
                                                backupCount=2)
warning_file_log.setLevel(logging.WARNING)
warning_file_log.setFormatter(file_formatter)
root_logger.addHandler(warning_file_log)

error_file_log = handlers.RotatingFileHandler(log_dir + "twitter_error.log", maxBytes=4 * 1024 * 1024, backupCount=2)
error_file_log.setLevel(logging.ERROR)
error_file_log.setFormatter(file_formatter)
root_logger.addHandler(error_file_log)

console_formatter = logging.Formatter('%(asctime)s [%(name)s] %(message)s')
console_log = logging.StreamHandler()
console_log.setLevel(logging.INFO)
console_log.setFormatter(console_formatter)
root_logger.addHandler(console_log)

