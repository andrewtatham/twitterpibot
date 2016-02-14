import logging
import os

from twython import Twython

from twitterpibot import Statistics
from twitterpibot.logic.FileSystemHelper import bytes_from_file
from twitterpibot.twitter import Authenticator
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.twitter.MyStreamer import MyStreamer

logger = logging.getLogger(__name__)
try:
    from urllib.parse import quote_plus
except ImportError:
    # noinspection PyUnresolvedReferences
    from urllib import quote_plus


class TwitterHelper(object):
    def __init__(self, identity):
        self.identity = identity
        if not self.identity.tokens:
            self.identity.tokens = Authenticator.get_tokens(identity.screen_name)
        self.twitter = Twython(
            self.identity.tokens[0],
            self.identity.tokens[1],
            self.identity.tokens[2],
            self.identity.tokens[3])
        self.identity.twid = self.twitter.lookup_user(screen_name=identity.screen_name)[0]["id_str"]

    def send(self, outbox_item):
        outbox_item.display()
        if type(outbox_item) is OutgoingTweet:

            if outbox_item.filePaths and any(outbox_item.filePaths):
                media_ids = []
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

            response = self.identity.twitter.update_status(
                status=outbox_item.status,
                in_reply_to_status_id=outbox_item.in_reply_to_status_id,
                media_ids=outbox_item.media_ids)
            Statistics.record_outgoing_tweet()
            id_str = response["id_str"]
            return id_str

        if type(outbox_item) is OutgoingDirectMessage:
            if not outbox_item.screen_name and not outbox_item.user_id:
                outbox_item.screen_name = self.identity.admin_screen_name
                outbox_item.user_id = self.identity.admin_user_id

            self.identity.twitter.send_direct_message(
                text=outbox_item.text,
                screen_name=outbox_item.screen_name,
                user_id=outbox_item.user_id)
            Statistics.record_outgoing_direct_message()
        return None

    def reply_with(self, inbox_item, text=None, as_tweet=False, as_direct_message=False, file_paths=None,
                   in_reply_to_status_id=None):
        reply_as_tweet = as_tweet or not as_direct_message and inbox_item.is_tweet

        reply_as_dm = as_direct_message or not as_tweet and inbox_item.is_direct_message

        if reply_as_tweet:
            tweet = OutgoingTweet(
                reply_to=inbox_item,
                text=text,
                file_paths=file_paths,
                in_reply_to_status_id=in_reply_to_status_id)
            return self.send(tweet)

        if reply_as_dm:
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
            return media["media_id_string"]
        finally:
            if file:
                file.close()

    def get_streamer(self, topic=None, topic_name=None):
        return MyStreamer(self.identity, topic, topic_name)

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
        for chunk in bytes_from_file(file_path, chunk_size):
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

    def create_favorite(self, id):
        self.twitter.create_favorite(id=id)
        Statistics.record_favourite()

    def retweet(self, id):
        self.twitter.retweet(id=id)
        Statistics.record_retweet()

    def add_user_to_list(self, list_id, user_id, screen_name):
        self.twitter.create_list_members(list_id=list_id, user_id=user_id, screen_name=screen_name)

    def block_user(self, user_id, user_screen_name):
        self.twitter.create_block(user_id=user_id, screen_name=user_screen_name)

    def get_user_timeline(self, user):
        return self.twitter.get_user_timeline(
            user_id=user.id,
            screen_name=user.screen_name,
            trim_user=True,
            count=20)

    def unblock_user(self, user):
        self.twitter.destroy_block(user_id=user.id, screen_name=user.screen_name)

    def unblock_users(self):

        user_ids = self.twitter.list_block_ids(stringify_ids=True)
        # pprint.pprint(user_ids["ids"])
        for user_id in user_ids["ids"]:
            print(user_id)
            self.twitter.destroy_block(user_id=user_id)

    def show_owned_lists(self):
        return self.twitter.show_owned_lists()["lists"]

    def get_list_members(self, list_id):
        return self.twitter.get_list_members(list_id=list_id)
