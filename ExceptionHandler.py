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
        args._RecordWarning(exception, None)

    def Handle(args, exception, context):
        if type(exception) is UnicodeEncodeError:
            args._RecordWarning(exception, context)
        else:
            args._RecordError(exception, context)


    def _RecordWarning(args, exception, context):
        print(Style.DIM + Fore.WHITE + Back.YELLOW + str(exception.message))
        logging.warn(exception)    
        if context:
            context.statistics.RecordWarning()

    def _RecordError(args, exception, context):
        print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
        logging.exception(exception)
        if context:
            context.statistics.RecordError()
        args._TrySendException(exception)

    def _TrySendException(args, exception):
        try:
            with MyTwitter() as twitter:
                twitter.send_direct_message(               
                    text = str(exception),
                    screen_name = "andrewtatham", 
                    user_id = "19201332")
        except Exception as e:
            pass
