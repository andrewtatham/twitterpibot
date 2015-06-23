import logging
from MyTwitter import MyTwitter
from Authenticator import Authenticator
from twython.exceptions import TwythonError

class ExceptionHandler(object):


    def HandleSilently(args, exception):
        logging.warn(exception)

    def Handle(args, exception):

        if type(exception) is UnicodeEncodeError:
            logging.warn(exception)

        elif type(exception) is TwythonError:
            if exception.message == "Twitter API returned a 403 (Forbidden), There was an error sending your message: Whoops! You already said that.":
                logging.warn(exception)
            else:
                print("*** EXCEPTION ***")
                logging.exception(exception)

                args.TrySendException(exception)


        else:
            print("*** EXCEPTION ***")
            logging.exception(exception)

            args.TrySendException(exception)




    def TrySendException(args, exception):
        

        try:
            tokens = Authenticator().Authenticate()
            twitter = MyTwitter(tokens[0], tokens[1], tokens[2], tokens[3])
      
            twitter.send_direct_message(               
                text = str(exception),
                screen_name = "andrewtatham", 
                user_id = "19201332")
            
        except Exception as e:
            pass

        

