from twython.streaming.api import TwythonStreamer
class MyStreamer(TwythonStreamer):
  
    def on_success(self, data):
        self.inbox.put(data)

            
    def on_error(self, status_code, data):
         
        msg = str(status_code) + " " + data
        logging.error(msg)
        print(msg)

