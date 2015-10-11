from twython.streaming.api import TwythonStreamer
import logging

class MyStreamer(TwythonStreamer):
  
    def on_success(self, data):
        global inbox
        inbox.put(data)
            
    def on_error(self, status_code, data):
        msg = str(status_code) + " " + str(data)
        logging.error(msg)
        print(msg)

        