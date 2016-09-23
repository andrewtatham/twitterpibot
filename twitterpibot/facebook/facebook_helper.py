import datetime
import logging
import pprint
import uuid
import facebook

from twitterpibot.data_access import dal

logger = logging.getLogger(__name__)


class FacebookHelper(object):
    def __init__(self, identity):
        self._identity = identity
        self._app_id = dal.get_token("facebook app id " + identity.screen_name)
        self._app_secret = dal.get_token("facebook app secret " + identity.screen_name)

        # https://developers.facebook.com/tools/explorer
        access_token_key = "facebook access token " + identity.screen_name
        # dal.set_token(access_token_key, "")
        self._access_token = dal.get_token(access_token_key)
        self._graph = facebook.GraphAPI(self._access_token)

        debug_access_token = self._graph.debug_access_token(self._access_token, self._app_id, self._app_secret)["data"]
        logger.info(pprint.pformat(debug_access_token))

        # TODO check
        is_valid = debug_access_token["is_valid"]
        scopes = debug_access_token["scopes"]
        expires_at = datetime.datetime.utcfromtimestamp(debug_access_token["expires_at"])
        logger.info("expires_at: {}".format(expires_at))
        expires_in = expires_at - datetime.datetime.utcnow()
        logger.info("expires_in: {}".format(expires_in))

        app_name = debug_access_token["application"]
        app_id = debug_access_token["app_id"]
        profile_id = debug_access_token["profile_id"]
        user_id = debug_access_token["user_id"]

        # profile = self._graph.get_object(profile_id)
        # logger.info(pprint.pformat(profile))
        #
        # app = self._graph.get_object(app_id)
        # logger.info(pprint.pformat(app))
        #
        # user = self._graph.get_object(user_id)
        # logger.info(pprint.pformat(user))

    def create_wall_post(self, post_text, attachment={}):
        if attachment is None:
            attachment = {}
        logger.info(post_text)
        wall_post = self._graph.put_wall_post(post_text, attachment=attachment)
        logger.debug(pprint.pformat(wall_post))
        return wall_post

    def create_comment(self, object_id, comment_text):
        comment = self._graph.put_comment(object_id, comment_text)
        logger.debug(pprint.pformat(comment))
        return comment

    def create_like(self, object_id):
        like = self._graph.put_like(object_id)
        logger.debug(pprint.pformat(like))
        return like

    def get_likes(self, object_id):
        likes = self._graph.get_connections(object_id, "likes")
        logger.debug(pprint.pformat(likes))
        return likes

    def get_comments(self, object_id):
        comments = self._graph.get_connections(object_id, "comments")
        logger.debug(pprint.pformat(comments))
        return comments

    def create_attachment(self, name=None, link=None, caption=None, description=None, picture=None):
        attachment = {}
        if name: attachment['name'] = name
        if link: attachment['link'] = link
        if caption: attachment['caption'] = caption
        if description: attachment['description'] = description
        if picture: attachment['picture'] = picture
        return attachment

    def create_wall_post_from_tweet(self, inbox_item, rt_or_fav):
        if inbox_item.medias:
            picture = inbox_item.medias[0].get_thumbnail()
        elif inbox_item.sender.profile_image_url:
            picture = inbox_item.sender.profile_image_url
        else:
            picture = None
        attachment = self.create_attachment(
            name="tweet by {} (@{})".format(
                inbox_item.sender.name,
                inbox_item.sender.screen_name),
            link=inbox_item.url,
            caption=inbox_item.url,
            description=inbox_item.sender.description,
            picture=picture)
        self.create_wall_post(
            post_text="{} @{}: \"{}\"".format(
                rt_or_fav, inbox_item.sender.screen_name, inbox_item.text),
            attachment=attachment)


if __name__ == '__main__':
    import identities

    logging.basicConfig(level=logging.INFO)

    identity = identities.AndrewTathamPiIdentity()

    post_text = "blah {}".format(uuid.uuid4())
    wall_post = identity.facebook.create_wall_post(post_text)

    comment_text = "comment {}".format(uuid.uuid4())
    identity.facebook.create_comment(wall_post["id"], comment_text)

    identity.facebook.create_like(wall_post["id"])

    likes = identity.facebook.get_likes(wall_post["id"])
    logger.info(pprint.pformat(likes))

    comments = identity.facebook.get_comments(wall_post["id"])
    logger.info(pprint.pformat(comments))
