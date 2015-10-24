import logging
from logging import handlers
import os
from twitterpibot.hardware import hardware

rootlogger = logging.getLogger("")

dir = "temp" + os.sep + "log" + os.sep 

if not os.path.exists(dir):
    os.makedirs(dir)

fh = handlers.RotatingFileHandler(dir + "twitter.log", maxBytes=1024, backupCount=2)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
if hardware.iswindows:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to rootlogger
rootlogger.addHandler(ch)
rootlogger.addHandler(fh)
