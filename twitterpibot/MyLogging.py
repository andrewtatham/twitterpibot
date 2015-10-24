import logging
from logging import handlers
import os

rootlogger = logging.getLogger("")

fh = handlers.RotatingFileHandler("temp" + os.pathsep + "log" + os.pathsep + "twitter.log", maxBytes=1024, backupCount=2)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to rootlogger
rootlogger.addHandler(ch)
rootlogger.addHandler(fh)
