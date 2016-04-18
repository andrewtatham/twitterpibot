import os
import re
from twitterpibot.logic import fsh

folder = fsh.root + "twitterpibot" + os.sep + "movies" + os.sep

x = [
    "[\d]+",
    "[\d]+:[\d]+:[\d]+,[\d]+ --> [\d]+:[\d]+:[\d]+,[\d]+",
    "Created and Encoded by",
    "Visiontext Subtitles",
    "Julie Clayton & Rob Colling",
    "ENGLISH",
    "Best watched using"
]

rx = re.compile("|".join(x), re.MULTILINE)

line_endings = {".", "?", "!"}


def _clean_stage2(lines):
    # attempt to correct where one *movie* line has been split into multiple *subtitle* lines
    cleaned = []
    temp = ""
    for line in lines:
        if temp:
            temp += " "
        temp += line

        if temp[-1:] in line_endings:
            cleaned.append(temp)
            temp = ""
    return cleaned


def _clean(lines):
    cleaned = _clean_stage1(lines)
    cleaned = _clean_stage2(cleaned)
    return cleaned


def _clean_stage1(lines):
    cleaned = []
    temp = ""
    for line in lines:
        # print(line)
        line_encoded = line.replace(os.linesep, "")
        if line_encoded:

            if rx.match(line_encoded):
                if temp:
                    cleaned.append(temp)
                temp = ""
            else:
                if temp:
                    temp += " "
                temp += line_encoded
    if temp:
        cleaned.append(temp)
    return cleaned


def _parse_subtitles_file(file_path):
    file = open(folder + file_path, mode='r')
    lines = file.readlines()
    file.close()
    lines_cleaned = _clean(lines)
    return lines_cleaned


def get_lines(movie_name):
    return _parse_subtitles_file(movie_name + os.extsep + "srt")
