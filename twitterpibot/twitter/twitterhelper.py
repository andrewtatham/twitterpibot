import logging
import os
import random
import time

from retrying import retry

from twython import Twython, TwythonError

import identities
from twitterpibot.exceptionmanager import is_timeout, blocked
from twitterpibot.logic import fsh, giphyhelper
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter import authorisationhelper, tweet_splitter
from twitterpibot.twitter.streamer import Streamer

logger = logging.getLogger(__name__)
try:
    from urllib.parse import quote_plus
except ImportError:
    # noinspection PyUnresolvedReferences
    from urllib import quote_plus

retry_args = dict(
    stop_max_attempt_number=3,
    wait_fixed=100,
    retry_on_exception=is_timeout
)


class RateLimits(object):
    def __init__(self, data):
        self._data = data

    def get(self, key):
        parts = key.split("/")
        resource = parts[1]
        remaining = self._data["resources"][resource][key]["remaining"]
        return remaining

    def set(self, key, remaining):
        parts = key.split("/")
        resource = parts[1]
        self._data["resources"][resource][key]["remaining"] = remaining

    def can(self, key):
        remaining = self.get(key)
        if remaining > 0:
            remaining -= 1  # assume a call will be made
            logger.debug("{} remaining calls {}".format(key, remaining))
            self.set(key, remaining)
            return True
        else:
            return False

    def display(self):
        keys = ["/statuses/user_timeline", "/users/lookup"]
        return str(dict(map(lambda key: (key, self.get(key)), keys)))


class TwitterHelper(object):
    def __init__(self, identity):
        self.identity = identity
        if not self.identity.tokens:
            self.identity.tokens = authorisationhelper.get_tokens(identity.screen_name)
        self.twitter = Twython(
            self.identity.tokens[0],
            self.identity.tokens[1],
            self.identity.tokens[2],
            self.identity.tokens[3]
        )
        # self.identity.twid = self.twitter.lookup_user(screen_name=identity.screen_name)[0]["id_str"]
        self.mutation = [" ,", " .", " *", " `", " -", " _"]

        self.twitter_configuration = self.twitter.get_twitter_configuration()

        logger.debug(self.twitter_configuration)
        giphyhelper.set_photo_size_limit(self.twitter_configuration["photo_size_limit"])

        me = self.twitter.lookup_user(screen_name=self.identity.screen_name)[0]
        logger.debug(me)
        self.identity.update(me)

        self.rates = None
        self.update_rate_limits()

    @retry(**retry_args)
    def send(self, outbox_item):
        if type(outbox_item) is OutgoingTweet:

            outbox_item.display()

            if outbox_item.filePaths and any(outbox_item.filePaths):
                for filePath in outbox_item.filePaths:
                    # ext = os.path.splitext(filePath)
                    # if ext == "mp4":
                    #     media_id = self._upload_video(filePath)
                    # else:
                    media_id = self._upload_media(filePath)
                    if media_id:
                        outbox_item.media_ids.append(media_id)

            split_tweets = tweet_splitter.split_tweet(outbox_item, self.twitter_configuration)

            in_reply_to_id_str = outbox_item.in_reply_to_id_str

            for split_tweet in split_tweets:
                split_tweet.in_reply_to_id_str = in_reply_to_id_str
                response = self.twitter.update_status(**split_tweet.get_tweet_params())
                split_tweet.id_str = response["id_str"]
                self.identity.conversations.outgoing(split_tweet)
                self.identity.statistics.record_outgoing_tweet()
                in_reply_to_id_str = split_tweet.id_str

            return in_reply_to_id_str

        if type(outbox_item) is OutgoingDirectMessage:
            if not outbox_item.screen_name and not outbox_item.user_id:
                outbox_item.screen_name = self.identity.admin_screen_name

            outbox_item.display()
            self.twitter.send_direct_message(
                text=outbox_item.text,
                screen_name=outbox_item.screen_name,
                user_id=outbox_item.user_id)
            self.identity.statistics.record_outgoing_direct_message()
        return None

    def quote_tweet(self, inbox_item, text=None, file_paths=None):
        reply_as_quote_tweet = inbox_item.is_tweet
        reply_as_dm = inbox_item.is_direct_message

        if reply_as_quote_tweet:
            logger.info("quoting to %s as quote tweet", inbox_item.text)
            tweet = OutgoingTweet(
                quote=inbox_item,
                text=text,
                file_paths=file_paths,
            )
            return self.send(tweet)

        if reply_as_dm:
            logger.info("replying to %s as DM", inbox_item.text)
            dm = OutgoingDirectMessage(
                reply_to=inbox_item,
                text=text)
            return self.send(dm)

        return None

    def reply_with(self, inbox_item, text=None, as_tweet=False, as_direct_message=False, file_paths=None,
                   in_reply_to_id_str=None):
        reply_as_tweet = as_tweet or not as_direct_message and inbox_item.is_tweet
        reply_as_dm = as_direct_message or not as_tweet and inbox_item.is_direct_message

        if reply_as_tweet:
            logger.info("replying to %s as tweet", inbox_item.text)
            tweet = OutgoingTweet(
                reply_to=inbox_item,
                text=text,
                file_paths=file_paths,
                in_reply_to_id_str=in_reply_to_id_str)
            return self.send(tweet)

        if reply_as_dm:
            logger.info("replying to %s as DM", inbox_item.text)
            dm = OutgoingDirectMessage(
                reply_to=inbox_item,
                text=text)
            return self.send(dm)

        return None

    def _upload_media(self, file_path):
        file = None
        try:
            file = open(file_path, 'rb')
            media = self.twitter.upload_media(media=file)
            self.identity.statistics.increment("Media Uploads")
            return media["media_id_string"]
        finally:
            if file:
                file.close()

    def get_streamer(self, topic=None, topic_name=None, responses=None, filter_level=None):
        return Streamer(self.identity, topic, topic_name, responses, filter_level)

    def _upload_video(self, file_path):
        logger.info('[MyTwitter] uploading ' + file_path)
        url = 'https://upload.twitter.com/1.1/media/upload.json'
        file_size = os.path.getsize(file_path)

        logger.info('[MyTwitter] Init')
        init_params = {
            "command": "INIT",
            "media_type": "video/mp4",
            "total_bytes": file_size
        }
        init_response = self.twitter.post(url, init_params)

        logger.info(init_response)

        media_id = init_response["media_id_string"]
        logger.info('[MyTwitter] media_id ' + media_id)

        segment = 0
        chunk_size = 4 * 1024 * 1024
        for chunk in fsh.bytes_from_file(file_path, chunk_size):
            logger.info('[MyTwitter] Append ' + str(segment))

            append_params = {
                'command': 'APPEND',
                'media_id': media_id,
                'segment_index': segment
            }
            append_response = self.twitter.post(url, append_params, {'media': chunk})

            logger.info(append_response)

        segment += 1

        logger.info('[MyTwitter] Finalize')
        finalize_params = {
            "command": "FINALIZE",
            "media_id": media_id,

        }
        self.twitter.post(url, finalize_params)

        return media_id

    def get_trending_topics_for(self, woeids):
        trending_topics = []
        for woeid in woeids:
            trends = self.twitter.get_place_trends(id=woeid)[0].get('trends', [])
            for trend in trends:
                trending_topics.append(trend['name'])
        return trending_topics

    def get_saved_searches(self):
        saved_searches = []
        searches = self.twitter.get_saved_searches()
        for srch in searches:
            saved_searches.append(srch['name'])
        return saved_searches

    def delete_saved_searches(self):
        searches = self.twitter.get_saved_searches()
        for srch in searches:
            self.twitter.destroy_saved_search(id=srch["id_str"])

    def search(self, text, result_type="popular"):
        query = quote_plus(text)
        return self.twitter.search(q=query, result_type=result_type)["statuses"]

    @retry(**retry_args)
    def favourite(self, id_str):
        try:
            self.twitter.create_favorite(id=id_str)
            self.identity.statistics.record_favourite()
        except TwythonError as ex:
            if "You have already favourited this tweet" in str(ex):
                logger.warning(ex)
            else:
                raise

    @retry(**retry_args)
    def retweet(self, id_str):
        try:
            self.twitter.retweet(id=id_str)
            self.identity.statistics.record_retweet()
        except TwythonError as ex:
            if "You have already retweeted this tweet" in str(ex):
                logger.warning(ex)
            else:
                raise

    @retry(**retry_args)
    def add_user_to_list(self, list_id, user_id, screen_name):
        self.twitter.create_list_members(list_id=list_id, user_id=user_id, screen_name=screen_name)

    @retry(**retry_args)
    def block_user(self, user_id, user_screen_name=None):
        self.twitter.create_block(user_id=user_id, screen_name=user_screen_name)

    @retry(**retry_args)
    def get_user_timeline(self, **kwargs):
        return self._rate_limit("/statuses/user_timeline", self.twitter.get_user_timeline, **kwargs)

    def unblock_user(self, user):
        self.twitter.destroy_block(user_id=user.id, screen_name=user.screen_name)

    @retry(**retry_args)
    def unblock_users(self):
        user_ids = self.twitter.list_block_ids(stringify_ids=True)
        for user_id in user_ids["ids"]:
            self.twitter.destroy_block(user_id=user_id)

    @retry(**retry_args)
    def show_owned_lists(self):
        return self.twitter.show_owned_lists()["lists"]

    @retry(**retry_args)
    def get_list_members(self, list_id):
        return self.twitter.get_list_members(list_id=list_id, count=5000, include_entities=False)

    @blocked
    @retry(**retry_args)
    def create_list(self, **kwargs):
        return self.twitter.create_list(**kwargs)

    @retry(**retry_args)
    def follow(self, user_id, screen_name):
        logger.info("following user id {} @{}".format(user_id, screen_name))
        self.twitter.create_friendship(user_id=user_id, screen_name=screen_name)
        self.identity.statistics.increment("Follows")

    @retry(**retry_args)
    def unfollow(self, user_id, screen_name):
        logger.info("unfollowing user id {} @{}".format(user_id, screen_name))
        self.twitter.destroy_friendship(user_id=user_id, screen_name=screen_name)
        self.identity.statistics.increment("Unfollows")

    @retry(**retry_args)
    def block(self, user_id, screen_name):
        logger.info("blocking user id {} @{}".format(user_id, screen_name))
        self.twitter.create_block(user_id=user_id, screen_name=screen_name)
        self.identity.statistics.increment("Blocks")

    @retry(**retry_args)
    def report(self, user_id, screen_name):
        logger.info("reporting user id {} @{}".format(user_id, screen_name))
        self.twitter.report_spam(user_id=user_id, screen_name=screen_name)
        self.identity.statistics.increment("Reports")

    @retry(**retry_args)
    def lookup_user(self, user_id):
        return self._rate_limit("/users/lookup", self.twitter.lookup_user, user_id=user_id)

    def sing_song(self, song, target=None, inbox_item=None, text=None, hashtag=None):
        if not text:
            text = random.choice(["All together now!", "Sing along!"])
        text += ' ' + song["video"]
        if hashtag:
            text += ' ' + hashtag

        in_reply_to_id_str = self._send_to(
            inbox_item=inbox_item,
            text=text,
            target=target,
            in_reply_to_id_str=None)
        time.sleep(5)

        lastlyrics = set([])
        for lyric in song["lyrics"]:
            lyric = lyric.strip()
            if lyric:
                if "<<screen_name>>" in lyric:
                    lyric = lyric.replace("<<screen_name>>", "@" + target)
                if hashtag:
                    lyric += " " + hashtag
                while lyric in lastlyrics:
                    lyric += random.choice(self.mutation)
                lastlyrics.add(lyric)
                self.identity.statistics.record_outgoing_song_lyric()
                in_reply_to_id_str = self._send_to(
                    inbox_item,
                    lyric,
                    target,
                    in_reply_to_id_str)
                time.sleep(5)

    def _send_to(self, inbox_item, text, target, in_reply_to_id_str):
        if inbox_item:
            return self.reply_with(
                inbox_item=inbox_item,
                text=text,
                in_reply_to_id_str=in_reply_to_id_str)
        else:
            status = ""
            if target:
                # noinspection PyUnresolvedReferences
                if isinstance(target, basestring):
                    status = ".@" + target
                elif isinstance(target, User.User):
                    status = ".@" + target.screen_name
            status += " " + text
            tweet = OutgoingTweet(
                text=status,
                in_reply_to_id_str=in_reply_to_id_str)
            return self.send(tweet)

    @retry(**retry_args)
    def get_list_subscriptions(self):
        return self.twitter.get_list_subscriptions()

    @retry(**retry_args)
    def subscribe_to_list(self, list_id):
        return self.twitter.subscribe_to_list(list_id=list_id)

    @retry(**retry_args)
    def geocode(self, location):
        result = self.twitter.search_geo(
            query=location.full_name,

            max_results=5,
            lat=location.latitude,
            long=location.longitude)
        logger.info(result)
        if result["result"]["places"]:
            # for place in result["result"]["places"]:
            #     logger.info(place["full_name"])

            place = result["result"]["places"][0]
            location.place_id_twitter = place["id"]

            return location
        else:
            return None

    @retry(**retry_args)
    def reverse_geocode(self, location):

        result = self.twitter.reverse_geocode(

            max_results=5,
            lat=location.latitude,
            long=location.longitude)
        logger.info(result)
        if result["result"]["places"]:
            # for place in result["result"]["places"]:
            #     logger.info(place["full_name"])

            place = result["result"]["places"][0]
            location.place_id_twitter = place["id"]

            return location
        else:
            return None

    @retry(**retry_args)
    def update_profile_image(self, file_path):
        if file_path:
            logger.info("updating profile image %s" % file_path)
            with open(file_path, 'rb') as file:
                self.twitter.update_profile_image(image=file)

    @retry(**retry_args)
    def update_profile_banner_image(self, file_path):
        if file_path:
            logger.info("updating banner image %s" % file_path)
            with open(file_path, 'rb') as file:
                try:
                    self.twitter.update_profile_banner_image(banner=file)
                except TwythonError as ex:
                    if "Response was not valid JSON" in str(ex):
                        # twython issue i think
                        logger.warning(ex)
                    else:
                        raise

    @retry(**retry_args)
    def update_profile(self, **kwargs):
        return self.twitter.update_profile(**kwargs)

    @retry(**retry_args)
    def get_list_statuses(self, **kwargs):
        return self.twitter.get_list_statuses(**kwargs)

    @retry(**retry_args)
    def get_user_suggestions_by_slug(self, **kwargs):
        return self.twitter.get_user_suggestions_by_slug(**kwargs)

    @retry(**retry_args)
    def get_user_suggestions(self, **kwargs):
        return self.twitter.get_user_suggestions(**kwargs)

    @retry(**retry_args)
    def lookup_status(self, **kwargs):
        return self.twitter.lookup_status(**kwargs)

    @retry(**retry_args)
    def get_followers(self, **kwargs):
        kwargs["stringify_ids"] = True
        followers = set()
        cursor = -1
        while cursor != "0":
            kwargs["cursor"] = cursor
            logger.info("getting followers")
            response = self.twitter.get_followers_ids(**kwargs)
            cursor = response["next_cursor_str"]
            followers = followers.union(set(response["ids"]))

        return followers

    @retry(**retry_args)
    def get_following(self, **kwargs):
        kwargs["stringify_ids"] = True
        following = set()
        cursor = -1
        while cursor != "0":
            kwargs["cursor"] = cursor
            logger.info("getting following")
            response = self.twitter.get_friends_ids(**kwargs)
            cursor = response["next_cursor_str"]
            following = following.union(set(response["ids"]))
        return following

    @retry(**retry_args)
    def update_rate_limits(self):
        data = self.twitter.get_application_rate_limit_status()
        self.rates = RateLimits(data)
        logger.info("Updated rate limits for {}: {}".format(self.identity.screen_name, self.rates.display()))

    def _rate_limit(self, limit_name, func, *args, **kwargs):
        if self.rates.can(limit_name):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                logger.warning(ex)
                return None
        else:
            logger.warning("{} limit exceeded".format(limit_name))
            return None

    @retry(**retry_args)
    def get_statuses(self, id_strs):
        id_strs_csv = ",".join(id_strs)
        return self.twitter.lookup_status(id=id_strs_csv)

    @retry(**retry_args)
    def get_status(self, id_str):
        return self.twitter.show_status(id=id_str)


if __name__ == "__main__":
    import identities_pis

    identity = identities.AndrewTathamIdentity()
    twitter = TwitterHelper(identity)
    # pprint.pprint(twitter.twitter_configuration)

    twitter.get_following()

    # slugs = twitter.get_user_suggestions()
    # pprint.pprint(slugs)
    # slug = random.choice(slugs)["slug"]
    # pprint.pprint(twitter.get_user_suggestions_by_slug(slug=slug))
