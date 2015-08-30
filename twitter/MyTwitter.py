from twython.api import Twython
from Authenticator import Authenticator
import tempfile
import cv2
import os
class MyTwitter(object):
    def __init__(self, *args, **kwargs):
        authenticator = Authenticator()
        tokens = authenticator.Authenticate()
        self.twython = Twython(tokens[0],tokens[1],tokens[2],tokens[3])
        

    def UploadMedia(args, photos):
        media_ids = []
        for photo in photos:
            if photo and photo.image is not None :
                try:
                    temp = None
                    try:
                        temp = tempfile.NamedTemporaryFile(suffix='.jpg',delete=False)
                        print('saving ' + temp.name)
                        cv2.imwrite(temp.name, photo.image)
                    finally:
                        if temp:
                            if not temp.close_called:
                                temp.close()

                    try:
                        f = open(temp.name,'rb')
                        print('uploading')
                        media = args.twython.upload_media(media=f)
                        media_id = media["media_id_string"]
                        if media_id :
                            print('media_id = ' + media_id)
                            media_ids.append(media_id)
                    finally:
                        if f:
                            if not f.closed:
                                f.close() 
                finally:
                    if temp:               
                        if os.path.exists(temp.name):
                            print('removing ' + temp.name)
                            os.remove(temp.name)
        
        return media_ids
    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.twython = None

    def get_application_rate_limit_status(self, **params):
        return self.twython.get_application_rate_limit_status(**params)

    def get_user_suggestions(self, **params):
        return self.twython.get_user_suggestions(**params)

    def get_user_suggestions_by_slug(self, **params):
        return self.twython.get_user_suggestions_by_slug(**params)


    def get_place_trends(self, **params):
        return self.twython.get_place_trends(**params)


    def upload_media(self, **params):
        return self.twython.upload_media(**params)

    def search(self, **params):
        return self.twython.search(**params)

    def update_status(self, **params):
        return self.twython.update_status(**params)

    def send_direct_message(self, **params):
        return self.twython.send_direct_message(**params)
    def create_favourite(self, **params):
        return self.twython.create_favorite(**params)
    def retweet(self, **params):
        return self.twython.retweet(**params)


    def show_owned_lists(self, **params):
        return self.twython.show_owned_lists(**params)

    def get_list_members(self, **params):
        return self.twython.get_list_members(**params)
    def create_block(self, **params):
        return self.twython.create_block(**params)
    def get_user_timeline(self, **params):
        return self.twython.get_user_timeline(**params)    
    def get_followers_list(self, **params):
        return self.twython.get_followers_list(**params)

        