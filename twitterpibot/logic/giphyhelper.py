import logging
import pprint
import giphypop

logger = logging.getLogger(__name__)

g = None
_init = False


def init():
    global _init
    global g
    if not _init:
        g = giphypop.Giphy()
        _init = True


def get_random_gif(text=None):
    init()
    gif = None
    if text:
        gif = g.translate(text)
    if not gif:
        gif = g.random_gif()

    url = _get_best_url(gif)
    return url


def get_gif(text):
    init()
    gif = g.translate(text)
    url = _get_best_url(gif)
    return url


def _get_format(version):
    if version:
        # todo enable webp/mp4 - requires twython upload video
        # if int(version.get("webp_size")) <= _max_image_size:
        #     return version.get("webp")
        # if int(version.get("mp4_size")) <= _max_image_size:
        #     return version.get("mp4_size")
        if int(version.get("size")) <= _max_image_size:
            return version.get("url")


def _get_best_url(gif):
    version = "original"
    url = _get_format(gif.get("original"))
    if not url:
        version = "downsized_large"
        url = _get_format(gif.get("raw_data").get("images").get("downsized_large"))
    if not url:
        version = "downsized_medium"
        url = _get_format(gif.get("raw_data").get("images").get("downsized_medium"))
    if not url:
        version = "downsized"
        url = _get_format(gif.get("raw_data").get("images").get("downsized"))
    if url:
        logger.info("{} {}".format(version, url))
    else:
        logger.warning("could not find suitable version: {}".format(pprint.pformat(gif)))
    return url


_max_image_size = 3145728


def set_photo_size_limit(photo_size_limit):
    global _max_image_size
    _max_image_size = int(photo_size_limit)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    pprint.pprint(get_gif("eggs"))

    pprint.pprint(get_random_gif())
