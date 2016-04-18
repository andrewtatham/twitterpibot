import logging
import giphypop

logger = logging.getLogger(__name__)

g = giphypop.Giphy()


def get_random_gif(text=None):
    gif = None
    if text:
        gif = g.translate(text)
    if not gif:
        gif = g.random_gif()

    url = _get_best_url(gif)
    return url





def get_gif(text):
    gif = g.translate(text)
    url = _get_best_url(gif)
    return url


def _get_format(version):
    if version:
        if int(version.get("webp_size")) <= _max_image_size:
            return version.get("webp")
        if int(version.get("mp4_size")) <= _max_image_size:
            return version.get("mp4_size")
        if int(version.get("size")) <= _max_image_size:
            return version.get("url")


def _get_best_url(gif):
    url = _get_format(gif.get("original"))
    if not url:
        url = _get_format(gif.get("raw_data").get("images").get("downsized_large"))
    if not url:
        url = _get_format(gif.get("raw_data").get("images").get("downsized_medium"))
    if not url:
        url = _get_format(gif.get("raw_data").get("images").get("downsized"))
    return url
_max_image_size = 3145728


def set_photo_size_limit(photo_size_limit):
    global _max_image_size
    _max_image_size = int(photo_size_limit)

if __name__ == '__main__':
    print(get_random_gif())
