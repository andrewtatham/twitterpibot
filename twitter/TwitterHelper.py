
from MyTwitter import MyTwitter
from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage
from Statistics import RecordOutgoingDirectMessage, RecordOutgoingTweet
from MyStreamer import MyStreamer

_screen_name = None
def Init(screen_name):
    global _screen_name
    _screen_name = screen_name
    with MyTwitter(_screen_name) as twitter:   
        me = twitter.lookup_user(screen_name = screen_name)[0]
        return me["id_str"]

def Send(outboxItem):
    outboxItem.Display()
    response = None
    with MyTwitter() as twitter:
        if type(outboxItem) is OutgoingTweet:

            RecordOutgoingTweet()

            if outboxItem.filePaths and any(outboxItem.filePaths):
                outboxItem.media_ids = _UploadMedia(twitter, outboxItem.filePaths)

            response = twitter.update_status(
                status = outboxItem.status,
                in_reply_to_status_id = outboxItem.in_reply_to_status_id,
                media_ids = outboxItem.media_ids)

        if type(outboxItem) is OutgoingDirectMessage:

            RecordOutgoingDirectMessage()         
                       
            response = twitter.send_direct_message(
                text = outboxItem.text, 
                screen_name = outboxItem.screen_name, 
                user_id = outboxItem.user_id)

    id_str = response["id_str"]
    return id_str

def ReplyWith(inboxItem, text, asTweet=False, asDM=False, filePaths=None, in_reply_to_status_id = None, *args, **kwargs):    

    replyAsTweet = asTweet or not asDM and inboxItem.isTweet

    replyAsDM = asDM or not asTweet and inboxItem.isDirectMessage

    if replyAsTweet :
        tweet = OutgoingTweet(
            replyTo=inboxItem,
            text=text,                
            filePaths = filePaths,
            in_reply_to_status_id = in_reply_to_status_id)
        return Send(tweet)
           
    if replyAsDM:
        dm = OutgoingDirectMessage(
            replyTo=inboxItem,
            text=text)
        return Send(dm)

    return None
    
def _UploadMedia(twitter, filePaths):
    media_ids = []
    for filePath in filePaths:
        try:
            file = open(filePath,'rb')
            media = twitter.upload_media(media=file)
            media_ids.append(media["media_id_string"])
        finally:
            file.close()
    return media_ids
 
def GetStreamer(screen_name):    
    return MyStreamer(screen_name)

