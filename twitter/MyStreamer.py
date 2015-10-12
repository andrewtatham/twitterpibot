from twython.streaming.api import TwythonStreamer
import logging
import MyQueues
class MyStreamer(TwythonStreamer):
  
    def on_success(self, data):
        MyQueues.inbox.put(data)
            
    def on_error(self, status_code, data):
        msg = str(status_code) + " " + str(data)
        logging.error(msg)
        print(msg)

        