import logging

from colorama import Fore, Style

from twitterpibot.twitter import Lists
from twitterpibot.twitter.MyTwitter import MyTwitter
from twitterpibot.twitter.topics import Topics

logger = logging.getLogger(__name__)


class BotBlocker(object):
    def IsUserBot(self, user):
        block_follower = False

        if not user.following and not user.verified:

            search_text = ""
            if user.name:
                search_text += user.name
            if user.screen_name:
                search_text += " " + user.screen_name
            if user.description:
                search_text += " " + user.description

            logger.info("Checking user profile: " + search_text)

            topics1 = Topics.get_topics(search_text)
            if topics1:
                logger.info("Profile topics:" + str(topics1))
                block_follower = topics1.spam()

            if not block_follower and (user.following or not user.protected):

                with MyTwitter() as twitter:
                    last_tweets = twitter.get_user_timeline(user_id=user.id,
                                                            screen_name=user.screen_name,
                                                            trim_user=True,
                                                            count=20)
                search_text = ""
                for tweet in last_tweets:
                    search_text += tweet["text"]
                logger.info("Checking user tweets" + search_text)
                topics2 = Topics.get_topics(search_text)
                if topics2:
                    logger.info("User tweet topics" + str(topics2))
                    block_follower = topics2.spam()
        return block_follower

    def BlockUser(self, user):
        txt = "[Botblock] BLOCKED: "
        if user.name:
            txt += user.name + " "
        if user.screen_name:
            txt += "[@" + user.screen_name + "] "
        if user.description:
            txt += "- " + user.description
        print(Fore.RED + Style.BRIGHT + txt)

        logger.warn(txt)
        Lists.add_user(list_name="Bad Bots", user_id=user.id, screen_name=user.screen_name)
        with MyTwitter() as twitter:
            twitter.create_block(user_id=user.id,
                                 screen_name=user.screen_name)

