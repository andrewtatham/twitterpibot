import os
import traceback

from PIL import Image, ImageDraw, ImageFont
from twitterpibot import hardware

from twitterpibot.logic import fsh

folder = fsh.root + "temp" + os.sep + "images" + os.sep + "text_on_an_image" + os.sep

positions = ["top-left", "top-right", "centre", "bottom-left", "bottom-right"]


def _get_rect(origin, size):
    return origin + tuple(map(sum, zip(origin, size)))


def put_text_on_an_image(image_path, exception=None, bold_text=None, text=None, text_position="centre"):
    base = Image.open(image_path).convert("RGBA")
    size = (1024, 768)
    base.thumbnail(size, Image.ANTIALIAS)

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

    # get a font
    if hardware.is_raspberry_pi_2:
        lrg_fnt = ImageFont.truetype('FreeSerif.ttf', 24)
        fnt = ImageFont.truetype('FreeSans.ttf', 12)
    elif hardware.is_mac_osx:
        lrg_fnt = ImageFont.truetype('Georgia Italic.ttf', 24)
        fnt = ImageFont.truetype('Arial.ttf', 12)
    else:
        lrg_fnt = ImageFont.truetype('Times New Roman.ttf', 24)
        fnt = ImageFont.truetype('Arial.ttf', 12)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    x = base.size[0]
    y = base.size[1]
    edge = 8

    # bg_rect = [(edge, edge), (x - edge, y - edge)]
    # bg_fill = (0, 0, 0, 64)
    # d.rectangle(bg_rect, bg_fill)

    if exception:
        bold_text = str(exception)
        text = traceback.format_exc()

    if bold_text:
        bold_text = bold_text.strip()
        bold_text_bg_size = d.textsize(bold_text, lrg_fnt)
        bold_text_bg_origin = (edge, edge)
        bold_text_bg_rect = _get_rect(bold_text_bg_origin, bold_text_bg_size)
        bold_text_bg_fill = (0, 0, 0, 128)
        d.rectangle(bold_text_bg_rect, bold_text_bg_fill)
        d.text(bold_text_bg_origin, bold_text, font=lrg_fnt, fill=(255, 255, 255, 196))

    if text:
        text = text.strip()
        text_bg_size = d.textsize(text, fnt)
        text_bg_origin = None
        if not text_position:
            text_position = "centre"
        if text_position == "top-left":
            text_bg_origin = (edge, edge)
        if text_position == "top-right":
            text_bg_origin = (x - edge - text_bg_size[0], edge)
        if text_position == "centre":
            text_bg_origin = (x / 2 - edge - text_bg_size[0] / 2, y / 2 - edge - text_bg_size[1] / 2)
        if text_position == "bottom-left":
            text_bg_origin = (edge, y - edge - text_bg_size[1])
        if text_position == "bottom-right":
            text_bg_origin = (x - edge - text_bg_size[0], y - edge - text_bg_size[1])
        text_bg_rect = _get_rect(text_bg_origin, text_bg_size)
        text_bg_fill = (0, 0, 0, 128)
        d.rectangle(text_bg_rect, text_bg_fill)
        d.text(text_bg_origin, text, font=fnt, fill=(255, 255, 255, 196))

    out = Image.alpha_composite(base, txt)
    # out.show()
    out.save(image_path, decoder="jpg")
    return image_path
