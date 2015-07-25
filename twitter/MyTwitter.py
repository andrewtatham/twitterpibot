from twython.api import Twython
class MyTwitter(Twython):



    def get_application_rate_limit_status(self, **params):
        return super(MyTwitter, self).get_application_rate_limit_status(**params)

    def get_user_suggestions(self, **params):
        return super(MyTwitter, self).get_user_suggestions(**params)

    def get_user_suggestions_by_slug(self, **params):
        return super(MyTwitter, self).get_user_suggestions_by_slug(**params)


    def get_place_trends(self, **params):
        return super(MyTwitter, self).get_place_trends(**params)


    def upload_media(self, **params):
        return super(MyTwitter, self).upload_media(**params)

    def search(self, **params):
        return super(MyTwitter, self).search(**params)

    def update_status(self, **params):
        return super(MyTwitter, self).update_status(**params)

    def send_direct_message(self, **params):
        return super(MyTwitter, self).send_direct_message(**params)
