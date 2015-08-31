import logging
from MyTwitter import MyTwitter
from Authenticator import Authenticator
from twython.exceptions import TwythonError


import logging
from colorama import Fore, Style, Back

logging.basicConfig(filename='twitter.log',level=logging.INFO)

# "Twitter API returned a 429 (Too Many Requests), Rate limit exceeded"
# "Twitter API returned a 403 (Forbidden), There was an error sending your message: Whoops! You already said that."
class ExceptionHandler(object):


    def HandleSilently(args, exception):
        logging.warn(exception)

    def Handle(args, exception):

        if type(exception) is UnicodeEncodeError:
            print(Style.DIM + Fore.WHITE + Back.YELLOW + str(exception.message))
            logging.warn(exception)

        elif type(exception) is TwythonError:
            if exception.message == "Twitter API returned a 403 (Forbidden), There was an error sending your message: Whoops! You already said that.":
                print(Style.DIM + Fore.WHITE + Back.RED  + str(exception))
                logging.warn(exception)
            else:
                print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
                logging.exception(exception)

                args.TrySendException(exception)


        else:
            print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
            logging.exception(exception)

            args.TrySendException(exception)




    def TrySendException(args, exception):
        

        try:
       
            with MyTwitter() as twitter:
                twitter.send_direct_message(               
                    text = str(exception),
                    screen_name = "andrewtatham", 
                    user_id = "19201332")
            
        except Exception as e:
            pass

        

