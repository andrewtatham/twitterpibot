import os
import time
import tkinter

from PIL import Image, ImageDraw, ImageTk

from twitterpibot.logic import image_helper, fsh

pixel = 32
margin = 4
bg = (0, 0, 0)

image_size = (margin + 8 * (pixel + margin), margin + 8 * (pixel + margin))

img = Image.new('RGB', image_size, bg)
draw = ImageDraw.Draw(img)
_buffer = [[(0, 0, 0) for x in range(8)] for y in range(8)]


def set_pixel(x, y, r, g, b):
    _buffer[x][y] = (r, g, b)


image_number = 0


def show():
    global image_number

    for pixel_x in range(8):
        for pixel_y in range(8):
            rgb = _buffer[pixel_x][pixel_y]
            x = margin + pixel_x * (pixel + margin)
            y = margin + pixel_y * (pixel + margin)
            rect = image_helper.rectangle((x, y), (pixel, pixel))
            draw.ellipse(rect, rgb, rgb)
    path = folder + "image{}.BMP".format(image_number)
    img.save(path, "BMP")

    paths.append(path)
    image_number += 1


folder = fsh.root + "temp" + os.sep + "images" + os.sep + "unicorhat" + os.sep
fsh.ensure_directory_exists_and_is_empty(folder)

paths = []

label = None
root = None
photo = None


def change_image(path):
    global photo
    image = Image.open(path)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo  # keep a reference!
    label.pack()
    root.update()


def display():
    global root
    global label
    root = tkinter.Tk()

    label = tkinter.Label(root)
    label.pack()
    label.place(x=0, y=0)

    root.after(100, callback)
    root.mainloop()


def callback():
    run = True

    while run:
        try:
            for path in paths:
                print(path)
                change_image(path)
                time.sleep(0.1)
        except Exception:
            run = False
    fsh.ensure_directory_exists_and_is_empty(folder)
