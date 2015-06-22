class ResponseFactory(object):
    def __init__(self, *args, **kwargs):


        # INIT DEANPICS
        deanmessages = ["need moar", "many", "so much", "very", "wow"]
        picsfolder = "pics/"
        if not os.path.exists(picsfolder):
            os.makedirs(picsfolder)
        pics = {}
        people = os.listdir(picsfolder)
        for person in people:
            name = str(person)
            personpicsfolder = picsfolder + name + "/"
            if os.path.isdir(personpicsfolder):
                pics[name] = os.listdir(personpicsfolder)



       


        return super(ResponseFactory, self).__init__(*args, **kwargs)




class PhotoResponse(Response):
    def ReplyWithPhoto(sender):
        logging.info("taking photo...")
        path = TakePhoto()
        logging.info("uploading...")
        media = twitter.upload_media(media=open(path,"rb"))
        plogging.info.plogging.info(media)
        logging.info("tweeting...")
        photomessages = ["cheese!", "smile!"]
        tweet = OutgoingTweet()
        tweet.status = "@" + sender + " " + random.choice(photomessages)
        tweet.media_ids = media["media_id_string"]
        outbox.put(tweet)
        logging.info("done.")




class PictureResponse(Response):

    def Respond(sender=None, name=None):
    
        if name is None:
            name = random.choice(people)
        
        logging.info("getting " + name + " pic...")
        path = picsfolder + name + "/" + random.choice(pics[name])
        logging.info("uploading " + path + "...")
        media = twitter.upload_media(media=open(path,"rb"))
        logging.info("tweeting...")
        message = random.choice(deanmessages) + " " + name
    
        if sender :
            message = "@" + sender + " " + message 


        tweet = OutgoingTweet()
        tweet.status = message
        tweet.media_ids = media["media_id_string"]    
        outbox.put(tweet)

        logging.info("done.")


