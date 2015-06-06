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



        songsfolder = "songs/"
        songs = {}
        songfiles = os.listdir(songsfolder)
        for songfile in songfiles:
            songname = songfile.lower()
            if songname.endswith('.txt'):
                songname = songname[:-4]
            songs[songname] = open(songsfolder + songfile, "rb").readlines()


        return super(ResponseFactory, self).__init__(*args, **kwargs)


class Response(object):
    pass

    def Condition(args):
        return False

class HelpResponse(Response):
    pass

def ReplyWithHelp(context):

    helpText = 'blah blah help'

    ReplyWith(context, helpText)


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
    
        if sender is not None:
            message = "@" + sender + " " + message 


        tweet = OutgoingTweet()
        tweet.status = message
        tweet.media_ids = media["media_id_string"]    
        outbox.put(tweet)

        logging.info("done.")




class SongResponse(Response):
        
    def Respond(target, song):
    
        logging.info("getting " + song + " song...")
        lyrics = songs[song.lower()]
        lastlyric = ""
        for lyric in lyrics:
            lyric = lyric.strip()
            if lyric and lyric != lastlyric:
                tweettext = "@" + target + " " + lyric
                logging.info("tweeting: " + tweettext)
                tweet = OutgoingTweet()
                tweet.status = tweettext
                songTweetQueue.put(tweet)
                lastlyric = lyric
       
            
    
        logging.info("done.")