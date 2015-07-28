from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage
from Task import Task

class ProcessOutboxTask(Task):
    def onRun(args):
        
        try:
            outboxItem = args.context.outbox.get()

            outboxItem.Display()

            if type(outboxItem) is OutgoingTweet:

                if outboxItem.photos and any(outboxItem.photos):
                    outboxItem.media_ids = args.context.UploadMedia(outboxItem.photos)



                args.context.twitter.update_status(
                    status = outboxItem.status,
                    in_reply_to_status_id = outboxItem.in_reply_to_status_id,
                    media_ids = outboxItem.media_ids)

            if type(outboxItem) is OutgoingDirectMessage:

                args.context.twitter.send_direct_message(
                    text = outboxItem.text, 
                    screen_name = outboxItem.screen_name, 
                    user_id = outboxItem.user_id)

            # todo catch 403 error when same text sent

        finally:
            args.context.outbox.task_done()
        
