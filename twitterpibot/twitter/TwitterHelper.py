from twitterpibot.twitter.MyTwitter import MyTwitter
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.Statistics import RecordOutgoingDirectMessage, RecordOutgoingTweet
from MyStreamer import MyStreamer
import os

_screen_name = None


def Init(screen_name):
    global _screen_name
    _screen_name = screen_name
    with MyTwitter(_screen_name) as twitter:
        me = twitter.lookup_user(screen_name=screen_name)[0]
        return me["id_str"]


def Send(outboxItem):
    outboxItem.Display()
    response = None
    with MyTwitter() as twitter:
        if type(outboxItem) is OutgoingTweet:

            RecordOutgoingTweet()

            if outboxItem.filePaths and any(outboxItem.filePaths):
                media_ids = []
                for filePath in outboxItem.filePaths:
                    ext = os.path.splitext(filePath)
                    if ext == "mp4":
                        media_id = _UploadVideo(filePath)
                    else:
                        media_id = _UploadMedia(twitter, filePath)
                    if media_id:
                        media_ids.append(media_id)

                if media_ids:
                    outboxItem.media_ids = media_ids

            response = twitter.update_status(
                status=outboxItem.status,
                in_reply_to_status_id=outboxItem.in_reply_to_status_id,
                media_ids=outboxItem.media_ids)

        if type(outboxItem) is OutgoingDirectMessage:
            RecordOutgoingDirectMessage()

            response = twitter.send_direct_message(
                text=outboxItem.text,
                screen_name=outboxItem.screen_name,
                user_id=outboxItem.user_id)

    id_str = response["id_str"]
    return id_str


def ReplyWith(inboxItem, text, asTweet=False, asDM=False, filePaths=None, in_reply_to_status_id=None):
    replyAsTweet = asTweet or not asDM and inboxItem.isTweet

    replyAsDM = asDM or not asTweet and inboxItem.isDirectMessage

    if replyAsTweet:
        tweet = OutgoingTweet(
            replyTo=inboxItem,
            text=text,
            filePaths=filePaths,
            in_reply_to_status_id=in_reply_to_status_id)
        return Send(tweet)

    if replyAsDM:
        dm = OutgoingDirectMessage(
            replyTo=inboxItem,
            text=text)
        return Send(dm)

    return None


def _UploadMedia(twitter, filePath):
    file = None
    try:
        file = open(filePath, 'rb')
        media = twitter.upload_media(media=file)
        return media["media_id_string"]
    finally:
        if file:
            file.close()


def GetStreamer(screen_name):
    return MyStreamer(screen_name)


def _UploadVideo(filePath):
    print('[MyTwitter] uploading ' + filePath)

    with MyTwitter() as twitter:
        url = 'https://upload.twitter.com/1.1/media/upload.json'
        fileSize = os.path.getsize(filePath)

        print('[MyTwitter] Init')
        initParams = {
            "command": "INIT",
            "media_type": "video/mp4",
            "total_bytes": fileSize
        }
        initResponse = twitter.post(url, initParams)

        print(initResponse)

        media_id = initResponse["media_id_string"]
        print('[MyTwitter] media_id ' + media_id)

        segment = 0
        chunkSize = 4 * 1024 * 1024
        for chunk in bytes_from_file(filePath, chunkSize):
            print('[MyTwitter] Append ' + str(segment))

            appendParams = {
                'command': 'APPEND',
                'media_id': media_id,
                'segment_index': segment
            }
            appendResponse = twitter.post(url, appendParams, {'media': chunk})

            print(appendResponse)

        segment += 1

        print('[MyTwitter] Finalize')
        finalizeParams = {
            "command": "FINALIZE",
            "media_id": media_id,

        }
        twitter.post(url, finalizeParams)

    return media_id


def bytes_from_file(filePath, chunksize):
    with open(filePath, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                yield chunk
            else:
                break