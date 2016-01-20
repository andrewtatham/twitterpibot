import logging
from twitterpibot import Statistics
from twitterpibot.twitter.MyTwitter import MyTwitter
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.twitter.MyStreamer import MyStreamer
import os

logger = logging.getLogger(__name__)
try:
    from urllib.parse import quote_plus
except ImportError:
    # noinspection PyUnresolvedReferences
    from urllib import quote_plus


_screen_name = None


def init(screen_name):
    global _screen_name
    _screen_name = screen_name
    with MyTwitter(_screen_name) as twitter:
        me = twitter.lookup_user(screen_name=_screen_name)[0]
        return me["id_str"]


def send(outbox_item):
    outbox_item.display()
    with MyTwitter() as twitter:
        if type(outbox_item) is OutgoingTweet:

            Statistics.record_outgoing_tweet()

            if outbox_item.filePaths and any(outbox_item.filePaths):
                media_ids = []
                for filePath in outbox_item.filePaths:
                    ext = os.path.splitext(filePath)
                    if ext == "mp4":
                        media_id = _upload_video(filePath)
                    else:
                        media_id = _upload_media(twitter, filePath)
                    if media_id:
                        media_ids.append(media_id)

                if media_ids:
                    outbox_item.media_ids = media_ids

            response = twitter.update_status(
                status=outbox_item.status,
                in_reply_to_status_id=outbox_item.in_reply_to_status_id,
                media_ids=outbox_item.media_ids)
            id_str = response["id_str"]
            return id_str

        if type(outbox_item) is OutgoingDirectMessage:
            Statistics.record_outgoing_direct_message()

            twitter.send_direct_message(
                text=outbox_item.text,
                screen_name=outbox_item.screen_name,
                user_id=outbox_item.user_id)

    return None


def reply_with(inbox_item, text, as_tweet=False, as_direct_message=False, file_paths=None, in_reply_to_status_id=None):
    reply_as_tweet = as_tweet or not as_direct_message and inbox_item.is_tweet

    reply_as_dm = as_direct_message or not as_tweet and inbox_item.is_direct_message

    if reply_as_tweet:
        tweet = OutgoingTweet(
            reply_to=inbox_item,
            text=text,
            file_paths=file_paths,
            in_reply_to_status_id=in_reply_to_status_id)
        return send(tweet)

    if reply_as_dm:
        dm = OutgoingDirectMessage(
            reply_to=inbox_item,
            text=text)
        return send(dm)

    return None


def _upload_media(twitter, file_path):
    file = None
    try:
        file = open(file_path, 'rb')
        media = twitter.upload_media(media=file)
        return media["media_id_string"]
    finally:
        if file:
            file.close()


def get_streamer(topic=None, topic_name=None):
    return MyStreamer(_screen_name, topic, topic_name)


def _upload_video(file_path):
    print('[MyTwitter] uploading ' + file_path)

    with MyTwitter() as twitter:
        url = 'https://upload.twitter.com/1.1/media/upload.json'
        file_size = os.path.getsize(file_path)

        logger.info('[MyTwitter] Init')
        init_params = {
            "command": "INIT",
            "media_type": "video/mp4",
            "total_bytes": file_size
        }
        init_response = twitter.post(url, init_params)

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
            append_response = twitter.post(url, append_params, {'media': chunk})

            logger.info(append_response)

        segment += 1

        logger.info('[MyTwitter] Finalize')
        finalize_params = {
            "command": "FINALIZE",
            "media_id": media_id,

        }
        twitter.post(url, finalize_params)

    return media_id


def bytes_from_file(file_path, chunk_size):
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


def get_trending_topics_for(woeids):
    trending_topics = []
    with MyTwitter() as twitter:
        for woeid in woeids:
            trends = twitter.get_place_trends(id=woeid)[0].get('trends', [])
            for trend in trends:
                trending_topics.append(trend['name'])
    return trending_topics


def get_saved_searches():
    saved_searches = []
    with MyTwitter() as twitter:
        searches = twitter.get_saved_searches()
        for srch in searches:
            saved_searches.append(srch['name'])
    return saved_searches


def delete_saved_searches():
    with MyTwitter() as twitter:
        searches = twitter.get_saved_searches()
        for srch in searches:
            twitter.destroy_saved_search(id=srch["id_str"])


def search(text, result_type="popular"):
    query = quote_plus(text)

    with MyTwitter() as twitter:
        return twitter.search(q=query, result_type=result_type)["statuses"]


def create_favorite(id):
    with MyTwitter() as twitter:
        twitter.create_favorite(id=id)
    Statistics.record_favourite()


def retweet(id):
    with MyTwitter() as twitter:
        twitter.retweet(id=id)
    Statistics.record_retweet()


def add_user_to_list(list_id, user_id, screen_name):
    with MyTwitter() as twitter:
        twitter.create_list_members(list_id=list_id, user_id=user_id, screen_name=screen_name)
