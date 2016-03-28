import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

from twitterpibot import hardware
from twitterpibot.logic import image_helper
from twitterpibot.logic.image_helper import rgb_to_hsv, hsv_to_rgb, rectangle

__author__ = 'andrewtatham'

if hardware.is_raspberry_pi_2:
    lrg_fnt = ImageFont.truetype('FreeSerif.ttf', 24)
    fnt = ImageFont.truetype('FreeSans.ttf', 12)
elif hardware.is_mac_osx:
    lrg_fnt = ImageFont.truetype('Georgia Italic.ttf', 24)
    fnt = ImageFont.truetype('Arial.ttf', 12)
else:
    lrg_fnt = ImageFont.truetype('Times New Roman.ttf', 24)
    fnt = ImageFont.truetype('Arial.ttf', 12)


def make(board, solution):
    l = 200
    x = l
    y = l
    image_size = (x, y)
    margin = 5

    n = 4

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    h, s, v = rgb_to_hsv(r, g, b)
    r, g, b = hsv_to_rgb(h, s, v)

    a = 128

    bg_colour = (r, g, b, a)
    r, g, b = hsv_to_rgb(h, s + 0.2, v + 10)
    bg_light_colour = (r, g, b, a)
    r, g, b = hsv_to_rgb(h, s - 0.2, v - 10)
    bg_dark_colour = (r, g, b, a)

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    h, s, v = rgb_to_hsv(r, g, b)
    r, g, b = hsv_to_rgb(h, s, v)

    hi_colour = (r, g, b, a)

    image = Image.new('RGBA', image_size, bg_colour)
    draw = ImageDraw.Draw(image)

    for colour in [bg_light_colour, bg_dark_colour]:
        for i in range(random.randint(1, 20)):
            origin = (random.randint(margin, x - margin), random.randint(margin, y - margin))
            size = (random.randint(0, 50), random.randint(0, 50))
            rect = image_helper.rectangle(origin, size)
            draw.ellipse(rect, fill=colour)

    board_image = None
    if board:
        board_image = Image.new('RGBA', image_size, (0, 0, 0, a))
        board_draw = ImageDraw.Draw(board_image)

        for row in range(n):
            for col in range(n):
                tile_origin = (row * 50, col * 50)
                tile_size = (45, 45)
                tile_rect = image_helper.rectangle(tile_origin, tile_size)
                tile_fill = bg_dark_colour
                letter = board[row][col]
                letter_size = board_draw.textsize(letter, lrg_fnt)
                board_draw.rectangle(tile_rect, tile_fill)
                board_draw.text(tile_origin, letter, font=lrg_fnt, fill=bg_dark_colour)

    solution_image = None
    if solution:
        solution_image = Image.new('RGBA', image_size, (0, 0, 0, a))
        solution_draw = ImageDraw.Draw(solution_image)

        text = " ".join(solution)
        text = textwrap.fill(text, 30)
        solution_draw.text((0, 0), text, font=fnt, fill=bg_light_colour)

        for word, path in solution.items():
            prev_point = None
            for tile in path:
                point = (
                    tile.row * 50 + random.randint(0, 5),
                    tile.col * 50 + random.randint(0, 5))
                if prev_point:
                    r = rectangle(prev_point, point)
                    solution_draw.line(r, width=len(word) - 2, fill=hi_colour)
                prev_point = point

    out = image
    if board_image:
        out = Image.alpha_composite(out, board_image)
    if solution_image:
        out = Image.alpha_composite(out, solution_image)
    # out.show()


if __name__ == '__main__':
    from twitterpibot.logic import botgle_solver
    board = [
        ['Y', 'B', 'N', 'O'],
        ['T', 'E', 'H', 'I'],
        ['F', 'O', 'A', 'R'],
        ['R', 'R', 'A', 'N']
    ]
    solution = botgle_solver.solve_board(board)
    make(board, solution)
