
def SongTweets():

    while running:
        try:
            tweet = songTweetQueue.get()            
            outbox.put(tweet)
            songTweetQueue.task_done()
            time.sleep(5)
        except Exception as e:
            logging.exception(e.message, e.args)             
            pprint.pprint(e)


