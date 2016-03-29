import logging
import os
import random
import textwrap
import time

from twython import Twython


from twitterpibot.logic import fsh
from twitterpibot.twitter import authorisationhelper
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.twitter.streamer import Streamer

logger = logging.getLogger(__name__)
try:
    from urllib.parse import quote_plus
except ImportError:
    # noinspection PyUnresolvedReferences
    from urllib import quote_plus


def _cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


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
        logger.info(self.twitter_configuration)

        me = self.twitter.lookup_user(screen_name=self.identity.screen_name)[0]
        logger.info(me)
        self.identity.id_str = me["id_str"]
        self.identity.profile_image_url = me["profile_image_url"]

    def send(self, outbox_item):
        if type(outbox_item) is OutgoingTweet:
            media_ids = []
            if outbox_item.filePaths and any(outbox_item.filePaths):
                for filePath in outbox_item.filePaths:
                    ext = os.path.splitext(filePath)
                    if ext == "mp4":
                        media_id = self._upload_video(filePath)
                    else:
                        media_id = self._upload_media(filePath)
                    if media_id:
                        media_ids.append(media_id)

                if media_ids:
                    outbox_item.media_ids = media_ids

            media_count = 0
            if outbox_item.media_ids:
                media_count = len(outbox_item.media_ids)

            link_count = 0  # TODO Count links

            outbox_item.display()

            in_reply_to_status_id = outbox_item.in_reply_to_status_id

            statuses = self._split_text(
                _cap(outbox_item.status, 140 * 100),
                link_count=link_count, image_count=media_count)

            line_number = 0
            for status in statuses:

                logger.info("status %s: %s chars: %s", line_number, len(status), status)

                tweet_params = {
                    "status": status,
                    "in_reply_to_status_id": in_reply_to_status_id,
                }

                if line_number == 0 and outbox_item.media_ids:
                    tweet_params["media_ids"] = outbox_item.media_ids
                if outbox_item.location:
                    tweet_params["lat"] = outbox_item.location.latitude,
                    tweet_params["long"] = outbox_item.location.longitude,
                    tweet_params["place_id"] = outbox_item.location.place_id_twitter

                response = self.twitter.update_status(**tweet_params)
                in_reply_to_status_id = response["id_str"]
                self.identity.statistics.record_outgoing_tweet()
                line_number += 1

            return in_reply_to_status_id

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

    def reply_with(self, inbox_item, text=None, as_tweet=False, as_direct_message=False, file_paths=None,
                   in_reply_to_status_id=None):
        reply_as_tweet = as_tweet or not as_direct_message and inbox_item.is_tweet
        reply_as_dm = as_direct_message or not as_tweet and inbox_item.is_direct_message

        if reply_as_tweet:
            logger.info("replying to %s as tweet", inbox_item.text)
            tweet = OutgoingTweet(
                reply_to=inbox_item,
                text=text,
                file_paths=file_paths,
                in_reply_to_status_id=in_reply_to_status_id)
            return self.send(tweet)

        if reply_as_dm:
            logger.info("replying to %s as DM", inbox_item.text)
            dm = OutgoingDirectMessage(
                reply_to=inbox_item,
                text=text)
            return self.send(dm)

        return None

    def _split_text(self, large_text, link_count=0, image_count=0):

        if link_count == 0 and image_count == 0 and len(large_text) <= 140:
            return [large_text]
        else:
            wrap_at = 140
            wrap_at -= image_count * self.twitter_configuration["characters_reserved_per_media"]
            wrap_at -= link_count * self.twitter_configuration["short_url_length_https"]

            lines = textwrap.wrap(large_text, 117)
            lines_count = len(lines)
            line_number = 0
            return_value = []
            for line in lines:
                is_continuation = lines_count > 1 and line_number != 0
                has_continuation = lines_count > 1 and line_number != lines_count - 1
                text = ""
                if is_continuation:
                    text += "..."
                text += line
                if has_continuation:
                    text += "..."
                return_value.append(text)
                line_number += 1
            return return_value

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
        logging.info('[MyTwitter] uploading ' + file_path)
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

    def create_favorite(self, status_id):
        self.twitter.create_favorite(id=status_id)
        self.identity.statistics.record_favourite()

    def retweet(self, status_id):
        self.twitter.retweet(id=status_id)
        self.identity.statistics.record_retweet()

    def add_user_to_list(self, list_id, user_id, screen_name):
        self.twitter.create_list_members(list_id=list_id, user_id=user_id, screen_name=screen_name)

    def block_user(self, user_id, user_screen_name):
        self.twitter.create_block(user_id=user_id, screen_name=user_screen_name)

    def get_user_timeline(self, **kwargs):
        return self.twitter.get_user_timeline(**kwargs)

    def unblock_user(self, user):
        self.twitter.destroy_block(user_id=user.id, screen_name=user.screen_name)

    def unblock_users(self):
        user_ids = self.twitter.list_block_ids(stringify_ids=True)
        for user_id in user_ids["ids"]:
            self.twitter.destroy_block(user_id=user_id)

    def show_owned_lists(self):
        return self.twitter.show_owned_lists()["lists"]

    def get_list_members(self, list_id):
        return self.twitter.get_list_members(list_id=list_id, count=5000, include_entities=False, skip_status=True)

    def create_list(self, name, mode):
        return self.twitter.create_list(name=name, mode=mode)

    def follow(self, screen_name=None, user_id=None):
        self.identity.statistics.increment("Follows")
        return self.twitter.create_friendship(screen_name=screen_name, user_id=user_id)

    def lookup_user(self, user_id):
        return self.twitter.lookup_user(user_id=user_id)

    def sing_song(self, song, target=None, inbox_item=None, text=None, hashtag=None):
        if not text:
            text = random.choice(["All together now!", "Sing along!"])
        text += ' ' + song["video"]
        if hashtag:
            text += ' ' + hashtag

        in_reply_to_status_id = self._send_to(
            inbox_item=inbox_item,
            text=text,
            target=target,
            in_reply_to_status_id=None)
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
                in_reply_to_status_id = self._send_to(
                    inbox_item,
                    lyric,
                    target,
                    in_reply_to_status_id)
                time.sleep(5)

    def _send_to(self, inbox_item, text, target, in_reply_to_status_id):
        if inbox_item:
            return self.reply_with(
                inbox_item=inbox_item,
                text=text,
                in_reply_to_status_id=in_reply_to_status_id)
        else:
            text = ""
            if target:
                # noinspection PyUnresolvedReferences
                if isinstance(target, basestring):
                    text = ".@" + target
                elif isinstance(target, User.User):
                    text = ".@" + target.screen_name
            text += " " + text
            tweet = OutgoingTweet(
                text=text,
                in_reply_to_status_id=in_reply_to_status_id)
            return self.send(tweet)

    def get_list_subscriptions(self):
        return self.twitter.get_list_subscriptions()

    def subscribe_to_list(self, list_id):
        return self.twitter.subscribe_to_list(list_id=list_id)

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


if __name__ == "__main__":
    import main
    twitter = TwitterHelper(main.AndrewTathamPiIdentity(main.AndrewTathamIdentity()))
