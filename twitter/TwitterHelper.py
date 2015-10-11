
from MyTwitter import MyTwitter
from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage
from Statistics import RecordOutgoingDirectMessage, RecordOutgoingTweet


def Send(outboxItem):
    outboxItem.Display()
    response = None
    with MyTwitter() as twitter:
        if type(outboxItem) is OutgoingTweet:
            RecordOutgoingTweet()
            if outboxItem.photos and any(outboxItem.photos):
                outboxItem.media_ids = twitter.UploadMedia(outboxItem.photos)
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

def ReplyWith(inboxItem, text, asTweet=False, asDM=False, photos=None, in_reply_to_status_id = None, *args, **kwargs):    

    replyAsTweet = asTweet or not asDM and inboxItem.isTweet

    replyAsDM = asDM or not asTweet and inboxItem.isDirectMessage

    if replyAsTweet :
        tweet = OutgoingTweet(
            replyTo=inboxItem,
            text=text,                
            photos = photos,
            in_reply_to_status_id = in_reply_to_status_id)
        return Send(tweet)
           
    if replyAsDM:
        dm = OutgoingDirectMessage(
            replyTo=inboxItem,
            text=text)
        return Send(dm)
