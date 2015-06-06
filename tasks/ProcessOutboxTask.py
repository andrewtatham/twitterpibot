def SendTweets():

    while running:
        try:
            outboxItem = outbox.get()  
            if type(outboxItem) is OutgoingTweet:
                twitter.update_status(outboxItem)
            if type(outboxItem) is OutgoingDirectMessage:
                twitter.send_direct_message(outboxItem)
            outbox.task_done()

        except Exception as e:
            print ('EXCEPTION SendTweets')
            logging.exception(e.message, e.args)             
            pprint.pprint(e)
