import random

from PIL import Image, ImageDraw, ImageFont

from twitterpibot import hardware
from twitterpibot.logic import image_helper
from twitterpibot.logic.image_helper import hsv_to_rgb

__author__ = 'andrewtatham'

if hardware.is_raspberry_pi_2:
    lrg_fnt = ImageFont.truetype('FreeSans.ttf', 36)
    fnt = ImageFont.truetype('FreeSans.ttf', 10)
elif hardware.is_mac_osx:
    lrg_fnt = ImageFont.truetype('Arial.ttf', 36)
    fnt = ImageFont.truetype('Arial.ttf', 10)
else:
    lrg_fnt = ImageFont.truetype('Arial.ttf', 36)
    fnt = ImageFont.truetype('Arial.ttf', 10)


def make(board, solution):
    retval = {}
    image_length = 230
    image_width = image_length
    image_height = image_length
    image_size = (image_width, image_height)
    margin = 2

    n = 4

    h = random.uniform(0.0, 1.0)
    s = 1.0
    v = 255

    h_range = random.uniform(0.2, 0.8)

    a = 255

    r, g, b = hsv_to_rgb(h, s, v / 3)
    bg_colour = (r, g, b, a)
    r, g, b = hsv_to_rgb(h, s, v / 4)
    bg_dark_colour = (r, g, b, a)

    image = Image.new('RGBA', image_size, bg_dark_colour)
    draw = ImageDraw.Draw(image)

    max_letter_size = max(max(map(lambda l: draw.textsize(l, lrg_fnt), ["QU", "M"])))
    tile_padding = 0
    tile_size = (max_letter_size + tile_padding, max_letter_size + tile_padding)

    tile_origins = []
    tile_centres = []
    for row in range(n):
        tile_origin_row = []
        tile_centres_row = []
        for col in range(n):
            tile_origin = (margin + row * (tile_size[0] + margin),
                           margin + col * (tile_size[1] + margin))
            tile_origin_row.append(tile_origin)
            tile_centre = (tile_origin[0] + tile_size[0] / 2, tile_origin[1] + tile_size[1] / 2)
            tile_centres_row.append(tile_centre)
        tile_origins.append(tile_origin_row)
        tile_centres.append(tile_centres_row)

    board_image = None
    if board:
        board_image = Image.new('RGBA', image_size, (r, g, b, 0))
        board_draw = ImageDraw.Draw(board_image)
        option = random.randint(0, 1)
        for row in range(n):
            for col in range(n):
                tile_origin = tile_origins[row][col]
                tile_rect = image_helper.rectangle(tile_origin, tile_size)
                letter = board[row][col]
                letter_size = board_draw.textsize(letter, lrg_fnt)
                letter_origin = (tile_origin[0] + tile_size[0] / 2 - letter_size[0] / 2 + tile_padding / 4,
                                 tile_origin[1] + tile_size[1] / 2 - letter_size[1] / 2 + tile_padding / 4)

                if option == 0:
                    # board_draw.rectangle(tile_rect, outline=bg_colour,fill=bg_colour)
                    board_draw.ellipse(tile_rect, outline=bg_colour, fill=bg_colour)
                    board_draw.text(letter_origin, letter, font=lrg_fnt, fill=bg_dark_colour)
                else:
                    # board_draw.rectangle(tile_rect, outline=bg_colour)
                    board_draw.ellipse(tile_rect, outline=bg_colour)

                    board_draw.text(letter_origin, letter, font=lrg_fnt, fill=bg_colour)

    solution_image = None
    if solution:
        solution_image = Image.new('RGBA', image_size, (r, g, b, 0))
        solution_draw = ImageDraw.Draw(solution_image)

        # text = " ".join(solution)
        # text = textwrap.fill(text, 30)
        # solution_draw.text((0, 0), text, font=fnt, fill=bg_light_colour)

        found_words = list(solution)
        found_words.sort(key=len)
        n = random.randint(1, 4)
        found_words = found_words[-n:]
        found_words.reverse()

        retval["name"] = " ".join(found_words)

        h_delta = h_range / len(found_words)

        offset = -len(found_words)
        for found_word in found_words:
            h = image_helper.h_delta(h, h_delta)
            path = solution[found_word]
            r, g, b = hsv_to_rgb(h, s, v)
            path_colour = (r, g, b, a)
            prev_point = None
            for tile in path:
                if isinstance(tile, tuple):
                    row = tile[1]
                    col = tile[2]
                else:
                    row = tile.row
                    col = tile.col
                tile_centre = tile_centres[row][col]

                point = (tile_centre[0] + offset,
                         tile_centre[1] + offset)
                # wobble = 3
                # point = (tile_centre[0] + random.randint(-wobble, wobble),
                #          tile_centre[1] + random.randint(-wobble, wobble))
                if prev_point:
                    # len(word) - 2,
                    solution_draw.line((prev_point, point),
                                       width=1,
                                       fill=path_colour)
                else:
                    point_size = (1, 1)
                    rect = (
                        (point[0] - point_size[0], point[1] - point_size[1]),
                        (point[0] + point_size[0], point[1] + point_size[1]))
                    solution_draw.ellipse(rect, fill=path_colour)
                prev_point = point

            offset += 2

    out = image
    if board_image:
        out = Image.alpha_composite(out, board_image)
    if solution_image:
        out = Image.alpha_composite(out, solution_image)
    out.show()
    out.save("botgle.png", "png")
    retval["file_path"] = "botgle.png"
    return retval


if __name__ == '__main__':
    board = [
        ['Y', 'B', 'N', 'O'],
        ['T', 'E', 'H', 'I'],
        ['F', 'O', 'A', 'R'],
        ['R', 'R', 'A', 'N']
    ]
    # solution = botgle_solver.solve_board(board)
    # pprint.pprint(solution)
    solution = {
        'AHET': [("A", 2, 2), ("H", 1, 2), ("E", 1, 1), ("T", 1, 0)],
        'AHEY': [("A", 2, 2), ("H", 1, 2), ("E", 1, 1), ("Y", 0, 0)],
        'AHIR': [("A", 2, 2), ("H", 1, 2), ("I", 1, 3), ("R", 2, 3)],
        'AHO': [("A", 2, 2), ("H", 1, 2), ("O", 0, 3)],
        'AION': [("A", 2, 2), ("I", 1, 3), ("O", 0, 3), ("N", 0, 2)],
        'AIR': [("A", 2, 2), ("I", 1, 3), ("R", 2, 3)],
        'AIRA': [("A", 2, 2), ("I", 1, 3), ("R", 2, 3), ("A", 3, 2)],
        'AIRAN': [("A", 2, 2), ("I", 1, 3), ("R", 2, 3), ("A", 3, 2), ("N", 3, 3)],
        'ANA': [("A", 2, 2), ("N", 3, 3), ("A", 3, 2)],
        'AOTEA': [("A", 3, 2), ("O", 2, 1), ("T", 1, 0), ("E", 1, 1), ("A", 2, 2)],
        'ARA': [("A", 2, 2), ("R", 2, 3), ("A", 3, 2)],
        'ARAIN': [("A", 3, 2), ("R", 2, 3), ("A", 2, 2), ("I", 1, 3), ("N", 0, 2)],
        'ARAR': [("A", 2, 2), ("R", 2, 3), ("A", 3, 2), ("R", 3, 1)],
        'ARHAR': [("A", 3, 2), ("R", 2, 3), ("H", 1, 2), ("A", 2, 2), ("R", 3, 1)],
        'ARIA': [("A", 3, 2), ("R", 2, 3), ("I", 1, 3), ("A", 2, 2)],
        'ARIAN': [("A", 3, 2), ("R", 2, 3), ("I", 1, 3), ("A", 2, 2), ("N", 3, 3)],
        'ARION': [("A", 2, 2), ("R", 2, 3), ("I", 1, 3), ("O", 0, 3), ("N", 0, 2)],
        'ARN': [("A", 2, 2), ("R", 2, 3), ("N", 3, 3)],
        'ARNA': [("A", 2, 2), ("R", 2, 3), ("N", 3, 3), ("A", 3, 2)],
        'ARO': [("A", 2, 2), ("R", 3, 1), ("O", 2, 1)],
        'AROAR': [("A", 2, 2), ("R", 3, 1), ("O", 2, 1), ("A", 3, 2), ("R", 2, 3)],
        'BEA': [("B", 0, 1), ("E", 1, 1), ("A", 2, 2)],
        'BEAN': [("B", 0, 1), ("E", 1, 1), ("A", 2, 2), ("N", 3, 3)],
        'BEAR': [("B", 0, 1), ("E", 1, 1), ("A", 2, 2), ("R", 2, 3)],
        'BEHN': [("B", 0, 1), ("E", 1, 1), ("H", 1, 2), ("N", 0, 2)],
        'BEN': [("B", 0, 1), ("E", 1, 1), ("N", 0, 2)],
        'BENI': [("B", 0, 1), ("E", 1, 1), ("N", 0, 2), ("I", 1, 3)],
        'BENO': [("B", 0, 1), ("E", 1, 1), ("N", 0, 2), ("O", 0, 3)],
        'BET': [("B", 0, 1), ("E", 1, 1), ("T", 1, 0)],
        'BEY': [("B", 0, 1), ("E", 1, 1), ("Y", 0, 0)],
        'BHAR': [("B", 0, 1), ("H", 1, 2), ("A", 2, 2), ("R", 2, 3)],
        'BHARA': [("B", 0, 1), ("H", 1, 2), ("A", 2, 2), ("R", 2, 3), ("A", 3, 2)],
        'BYE': [("B", 0, 1), ("Y", 0, 0), ("E", 1, 1)],
        'EAN': [("E", 1, 1), ("A", 2, 2), ("N", 3, 3)],
        'EAR': [("E", 1, 1), ("A", 2, 2), ("R", 2, 3)],
        'EARN': [("E", 1, 1), ("A", 2, 2), ("R", 2, 3), ("N", 3, 3)],
        'EFT': [("E", 1, 1), ("F", 2, 0), ("T", 1, 0)],
        'EOAN': [("E", 1, 1), ("O", 2, 1), ("A", 2, 2), ("N", 3, 3)],
        'FEAR': [("F", 2, 0), ("E", 1, 1), ("A", 2, 2), ("R", 2, 3)],
        'FEN': [("F", 2, 0), ("E", 1, 1), ("N", 0, 2)],
        'FENIAN': [("F", 2, 0), ("E", 1, 1), ("N", 0, 2), ("I", 1, 3), ("A", 2, 2), ("N", 3, 3)],
        'FET': [("F", 2, 0), ("E", 1, 1), ("T", 1, 0)],
        'FETOR': [("F", 2, 0), ("E", 1, 1), ("T", 1, 0), ("O", 2, 1), ("R", 3, 0)],
        'FEY': [("F", 2, 0), ("E", 1, 1), ("Y", 0, 0)],
        'FOE': [("F", 2, 0), ("O", 2, 1), ("E", 1, 1)],
        'FOEHN': [("F", 2, 0), ("O", 2, 1), ("E", 1, 1), ("H", 1, 2), ("N", 0, 2)],
        'FOR': [("F", 2, 0), ("O", 2, 1), ("R", 3, 0)],
        'FORA': [("F", 2, 0), ("O", 2, 1), ("R", 3, 1), ("A", 2, 2)],
        'FOT': [("F", 2, 0), ("O", 2, 1), ("T", 1, 0)],
        'FRA': [("F", 2, 0), ("R", 3, 1), ("A", 2, 2)],
        'FRAE': [("F", 2, 0), ("R", 3, 1), ("A", 2, 2), ("E", 1, 1)],
        'FRO': [("F", 2, 0), ("R", 3, 0), ("O", 2, 1)],
        'FROE': [("F", 2, 0), ("R", 3, 0), ("O", 2, 1), ("E", 1, 1)],
        'FROT': [("F", 2, 0), ("R", 3, 0), ("O", 2, 1), ("T", 1, 0)],
        'HAET': [("H", 1, 2), ("A", 2, 2), ("E", 1, 1), ("T", 1, 0)],
        'HAIN': [("H", 1, 2), ("A", 2, 2), ("I", 1, 3), ("N", 0, 2)],
        'HAINE': [("H", 1, 2), ("A", 2, 2), ("I", 1, 3), ("N", 0, 2), ("E", 1, 1)],
        'HAIR': [("H", 1, 2), ("A", 2, 2), ("I", 1, 3), ("R", 2, 3)],
        'HAN': [("H", 1, 2), ("A", 2, 2), ("N", 3, 3)],
        'HAO': [("H", 1, 2), ("A", 2, 2), ("O", 2, 1)],
        'HARARI': [("H", 1, 2), ("A", 2, 2), ("R", 3, 1), ("A", 3, 2), ("R", 2, 3), ("I", 1, 3)],
        'HARN': [("H", 1, 2), ("A", 2, 2), ("R", 2, 3), ("N", 3, 3)],
        'HARR': [("H", 1, 2), ("A", 2, 2), ("R", 3, 1), ("R", 3, 0)],
        'HEAR': [("H", 1, 2), ("E", 1, 1), ("A", 2, 2), ("R", 2, 3)],
        'HEFT': [("H", 1, 2), ("E", 1, 1), ("F", 2, 0), ("T", 1, 0)],
        'HEFTY': [("H", 1, 2), ("E", 1, 1), ("F", 2, 0), ("T", 1, 0), ("Y", 0, 0)],
        'HEN': [("H", 1, 2), ("E", 1, 1), ("N", 0, 2)],
        'HET': [("H", 1, 2), ("E", 1, 1), ("T", 1, 0)],
        'HEY': [("H", 1, 2), ("E", 1, 1), ("Y", 0, 0)],
        'HIA': [("H", 1, 2), ("I", 1, 3), ("A", 2, 2)],
        'HIN': [("H", 1, 2), ("I", 1, 3), ("N", 0, 2)],
        'HOAR': [("H", 1, 2), ("O", 2, 1), ("A", 2, 2), ("R", 2, 3)],
        'HOE': [("H", 1, 2), ("O", 2, 1), ("E", 1, 1)],
        'HOI': [("H", 1, 2), ("O", 0, 3), ("I", 1, 3)],
        'HOIN': [("H", 1, 2), ("O", 0, 3), ("I", 1, 3), ("N", 0, 2)],
        'HON': [("H", 1, 2), ("O", 0, 3), ("N", 0, 2)],
        'HONE': [("H", 1, 2), ("O", 0, 3), ("N", 0, 2), ("E", 1, 1)],
        'HONEY': [("H", 1, 2), ("O", 0, 3), ("N", 0, 2), ("E", 1, 1), ("Y", 0, 0)],
        'HORA': [("H", 1, 2), ("O", 2, 1), ("R", 3, 1), ("A", 2, 2)],
        'HOT': [("H", 1, 2), ("O", 2, 1), ("T", 1, 0)],
        'IAN': [("I", 1, 3), ("A", 2, 2), ("N", 3, 3)],
        'IAO': [("I", 1, 3), ("A", 2, 2), ("O", 2, 1)],
        'INBE': [("I", 1, 3), ("N", 0, 2), ("B", 0, 1), ("E", 1, 1)],
        'INBY': [("I", 1, 3), ("N", 0, 2), ("B", 0, 1), ("Y", 0, 0)],
        'INO': [("I", 1, 3), ("N", 0, 2), ("O", 0, 3)],
        'ION': [("I", 1, 3), ("O", 0, 3), ("N", 0, 2)],
        'IONE': [("I", 1, 3), ("O", 0, 3), ("N", 0, 2), ("E", 1, 1)],
        'IRA': [("I", 1, 3), ("R", 2, 3), ("A", 2, 2)],
        'IRAN': [("I", 1, 3), ("R", 2, 3), ("A", 2, 2), ("N", 3, 3)],
        'NAA': [("N", 3, 3), ("A", 2, 2), ("A", 3, 2)],
        'NAE': [("N", 3, 3), ("A", 2, 2), ("E", 1, 1)],
        'NAHOR': [("N", 3, 3), ("A", 2, 2), ("H", 1, 2), ("O", 2, 1), ("R", 3, 0)],
        'NAIN': [("N", 3, 3), ("A", 2, 2), ("I", 1, 3), ("N", 0, 2)],
        'NAIO': [("N", 3, 3), ("A", 2, 2), ("I", 1, 3), ("O", 0, 3)],
        'NAIR': [("N", 3, 3), ("A", 2, 2), ("I", 1, 3), ("R", 2, 3)],
        'NAR': [("N", 3, 3), ("A", 2, 2), ("R", 2, 3)],
        'NARINE': [("N", 3, 3), ("A", 2, 2), ("R", 2, 3), ("I", 1, 3), ("N", 0, 2), ("E", 1, 1)],
        'NARR': [("N", 3, 3), ("A", 2, 2), ("R", 3, 1), ("R", 3, 0)],
        'NEA': [("N", 0, 2), ("E", 1, 1), ("A", 2, 2)],
        'NEB': [("N", 0, 2), ("E", 1, 1), ("B", 0, 1)],
        'NEF': [("N", 0, 2), ("E", 1, 1), ("F", 2, 0)],
        'NEO': [("N", 0, 2), ("E", 1, 1), ("O", 2, 1)],
        'NET': [("N", 0, 2), ("E", 1, 1), ("T", 1, 0)],
        'NHAN': [("N", 0, 2), ("H", 1, 2), ("A", 2, 2), ("N", 3, 3)],
        'NOIR': [("N", 0, 2), ("O", 0, 3), ("I", 1, 3), ("R", 2, 3)],
        'OAR': [("O", 2, 1), ("A", 2, 2), ("R", 2, 3)],
        'OFT': [("O", 2, 1), ("F", 2, 0), ("T", 1, 0)],
        'OFTEN': [("O", 2, 1), ("F", 2, 0), ("T", 1, 0), ("E", 1, 1), ("N", 0, 2)],
        'OHIA': [("O", 0, 3), ("H", 1, 2), ("I", 1, 3), ("A", 2, 2)],
        'OHIO': [("O", 2, 1), ("H", 1, 2), ("I", 1, 3), ("O", 0, 3)],
        'OHO': [("O", 0, 3), ("H", 1, 2), ("O", 2, 1)],
        'ONE': [("O", 0, 3), ("N", 0, 2), ("E", 1, 1)],
        'ORA': [("O", 2, 1), ("R", 3, 1), ("A", 2, 2)],
        'ORARIAN': [("O", 2, 1),
                    ("R", 3, 1),
                    ("A", 3, 2),
                    ("R", 2, 3),
                    ("I", 1, 3),
                    ("A", 2, 2),
                    ("N", 3, 3)],
        'ORARION': [("O", 2, 1),
                    ("R", 3, 1),
                    ("A", 2, 2),
                    ("R", 2, 3),
                    ("I", 1, 3),
                    ("O", 0, 3),
                    ("N", 0, 2)],
        'ORF': [("O", 2, 1), ("R", 3, 0), ("F", 2, 0)],
        'RAH': [("R", 2, 3), ("A", 2, 2), ("H", 1, 2)],
        'RAIN': [("R", 2, 3), ("A", 2, 2), ("I", 1, 3), ("N", 0, 2)],
        'RAN': [("R", 2, 3), ("A", 2, 2), ("N", 3, 3)],
        'RANA': [("R", 2, 3), ("A", 2, 2), ("N", 3, 3), ("A", 3, 2)],
        'RHE': [("R", 2, 3), ("H", 1, 2), ("E", 1, 1)],
        'RHEA': [("R", 2, 3), ("H", 1, 2), ("E", 1, 1), ("A", 2, 2)],
        'RHETOR': [("R", 2, 3), ("H", 1, 2), ("E", 1, 1), ("T", 1, 0), ("O", 2, 1), ("R", 3, 0)],
        'RHINE': [("R", 2, 3), ("H", 1, 2), ("I", 1, 3), ("N", 0, 2), ("E", 1, 1)],
        'RHINO': [("R", 2, 3), ("H", 1, 2), ("I", 1, 3), ("N", 0, 2), ("O", 0, 3)],
        'RHO': [("R", 2, 3), ("H", 1, 2), ("O", 0, 3)],
        'RIA': [("R", 2, 3), ("I", 1, 3), ("A", 2, 2)],
        'RINE': [("R", 2, 3), ("I", 1, 3), ("N", 0, 2), ("E", 1, 1)],
        'RIO': [("R", 2, 3), ("I", 1, 3), ("O", 0, 3)],
        'ROAN': [("R", 3, 0), ("O", 2, 1), ("A", 2, 2), ("N", 3, 3)],
        'ROAR': [("R", 3, 0), ("O", 2, 1), ("A", 2, 2), ("R", 2, 3)],
        'ROE': [("R", 3, 0), ("O", 2, 1), ("E", 1, 1)],
        'ROEY': [("R", 3, 0), ("O", 2, 1), ("E", 1, 1), ("Y", 0, 0)],
        'ROHAN': [("R", 3, 0), ("O", 2, 1), ("H", 1, 2), ("A", 2, 2), ("N", 3, 3)],
        'ROT': [("R", 3, 0), ("O", 2, 1), ("T", 1, 0)],
        'ROTE': [("R", 3, 0), ("O", 2, 1), ("T", 1, 0), ("E", 1, 1)],
        'TEA': [("T", 1, 0), ("E", 1, 1), ("A", 2, 2)],
        'TEAN': [("T", 1, 0), ("E", 1, 1), ("A", 2, 2), ("N", 3, 3)],
        'TEAR': [("T", 1, 0), ("E", 1, 1), ("A", 2, 2), ("R", 2, 3)],
        'TEN': [("T", 1, 0), ("E", 1, 1), ("N", 0, 2)],
        'TENIO': [("T", 1, 0), ("E", 1, 1), ("N", 0, 2), ("I", 1, 3), ("O", 0, 3)],
        'TOA': [("T", 1, 0), ("O", 2, 1), ("A", 2, 2)],
        'TOE': [("T", 1, 0), ("O", 2, 1), ("E", 1, 1)],
        'TOHO': [("T", 1, 0), ("O", 2, 1), ("H", 1, 2), ("O", 0, 3)],
        'TOR': [("T", 1, 0), ("O", 2, 1), ("R", 3, 0)],
        'TORA': [("T", 1, 0), ("O", 2, 1), ("R", 3, 1), ("A", 2, 2)],
        'TORAH': [("T", 1, 0), ("O", 2, 1), ("R", 3, 1), ("A", 2, 2), ("H", 1, 2)],
        'TORAN': [("T", 1, 0), ("O", 2, 1), ("R", 3, 1), ("A", 2, 2), ("N", 3, 3)],
        'TYE': [("T", 1, 0), ("Y", 0, 0), ("E", 1, 1)],
        'YEA': [("Y", 0, 0), ("E", 1, 1), ("A", 2, 2)],
        'YEAH': [("Y", 0, 0), ("E", 1, 1), ("A", 2, 2), ("H", 1, 2)],
        'YEAN': [("Y", 0, 0), ("E", 1, 1), ("A", 2, 2), ("N", 3, 3)],
        'YEAR': [("Y", 0, 0), ("E", 1, 1), ("A", 2, 2), ("R", 2, 3)],
        'YEARA': [("Y", 0, 0), ("E", 1, 1), ("A", 2, 2), ("R", 2, 3), ("A", 3, 2)],
        'YEARN': [("Y", 0, 0), ("E", 1, 1), ("A", 2, 2), ("R", 2, 3), ("N", 3, 3)],
        'YEN': [("Y", 0, 0), ("E", 1, 1), ("N", 0, 2)],
        'YENI': [("Y", 0, 0), ("E", 1, 1), ("N", 0, 2), ("I", 1, 3)],
        'YEO': [("Y", 0, 0), ("E", 1, 1), ("O", 2, 1)],
        'YET': [("Y", 0, 0), ("E", 1, 1), ("T", 1, 0)]}

    image = make(board, solution)
    print(image["name"])
    print(image["file_path"])
