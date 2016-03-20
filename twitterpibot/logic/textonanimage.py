import os
import random
import traceback

from PIL import Image, ImageDraw, ImageFont

from twitterpibot.logic import fsh, googlehelper

folder = fsh.root + "temp" + os.sep + "images" + os.sep + "text_on_an_image" + os.sep


def _get_rect(origin, size):
    return origin + tuple(map(sum, zip(origin, size)))


def put_text_on_an_image(image_path, exception=None, bold_text=None, text=None):
    base = Image.open(image_path).convert("RGBA")
    size = (640, 480)
    base.thumbnail(size, Image.ANTIALIAS)

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))




    # get a font
    lrg_fnt = ImageFont.truetype('Georgia Italic.ttf', 24)
    fnt = ImageFont.truetype('Georgia Italic.ttf', 12)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    x = base.size[0]
    y = base.size[1]
    edge = 24
    line_spacing = 128

    bg_rect = [(edge, edge), (x - edge, y - edge)]
    bg_fill = (0, 0, 0, 64)
    d.rectangle(bg_rect, bg_fill)

    if exception:
        things = ["Uh-oh", "DOH"]
        bold_text = "{}: {}".format(random.choice(things), str(exception))
        text = traceback.format_exc()

    if bold_text:
        bold_text_bg_origin = (edge, edge)
        bold_text_bg_size = d.textsize(bold_text, lrg_fnt)

        bold_text_bg_rect = _get_rect(bold_text_bg_origin, bold_text_bg_size)
        bold_text_bg_fill = (0, 0, 0, 128)
        d.rectangle(bold_text_bg_rect, bold_text_bg_fill)
        d.text(bold_text_bg_origin, bold_text, font=lrg_fnt, fill=(255, 255, 255, 255))

    if text:
        d.multiline_text((edge, edge + line_spacing), text, font=fnt, fill=(255, 255, 255, 192))

    out = Image.alpha_composite(base, txt)
    out.show()
    out.save(image_path, decoder="jpg")


def handle_exception(ex):
    queries = [
        "sunset",
        "kitten",
        "kittens",
        "puppy",
        "puppies",
        "goat",
        "goats"
    ]
    query = random.choice(queries)

    images = googlehelper.get_search_images(query, 5)
    image_url = random.choice(images)

    file_path = fsh.download_file(folder, image_url, query + ".jpg")

    # file_path = fsh.root + "temp" + os.sep + "images" + os.sep + "text_on_an_image" + os.sep + "goats.jpg"
    put_text_on_an_image(file_path, exception=ex)


if __name__ == "__main__":

    try:
        print(1 / 0)
    except Exception as ex:
        handle_exception(ex)
