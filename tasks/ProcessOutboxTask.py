from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage
from Task import Task
from MyTwitter import MyTwitter
import sys

class ProcessOutboxTask(Task):
    def onRun(args):
        
        try:
            outboxItem = args.context.outbox.get()
            if outboxItem:
                outboxItem.Display()

                with MyTwitter() as twitter:
                    if type(outboxItem) is OutgoingTweet:
                        if outboxItem.photos and any(outboxItem.photos):
                            outboxItem.media_ids = twitter.UploadMedia(outboxItem.photos)
                        twitter.update_status(
                            status = outboxItem.status,
                            in_reply_to_status_id = outboxItem.in_reply_to_status_id,
                            media_ids = outboxItem.media_ids)
                        args.context.statistics.RecordOutgoingTweet()
                    if type(outboxItem) is OutgoingDirectMessage:
                        twitter.send_direct_message(
                            text = outboxItem.text, 
                            screen_name = outboxItem.screen_name, 
                            user_id = outboxItem.user_id)
                        args.context.statistics.RecordOutgoingDirectMessage()
                    # todo catch 403 error when same text sent

        finally:
            args.context.outbox.task_done()

    def onStop(args):
        args.context.outbox.put(None)
