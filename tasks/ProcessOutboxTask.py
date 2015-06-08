from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage
from Task import Task

class ProcessOutboxTask(Task):
    def onRun(args):
        
        outboxItem = args.Context.outbox.get()

        outboxItem.Display()

        if type(outboxItem) is OutgoingTweet:

            args.Context.twitter.update_status(
                status = outboxItem.status,
                in_reply_to_status_id = outboxItem.in_reply_to_status_id,
                media_ids = outboxItem.media_ids)

        if type(outboxItem) is OutgoingDirectMessage:

            args.Context.twitter.send_direct_message(
                text = outboxItem.text, 
                screen_name = outboxItem.screen_name, 
                user_id = outboxItem.user_id)

        # todo catch 403 error when same text sent
        args.Context.outbox.task_done()
        
