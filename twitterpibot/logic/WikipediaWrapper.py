import pprint
import random
import logging

import wikipedia


def _parse_heading(line):
    return "=" in line, line


def _parse_content_tree(page_content):
    current_heading = "None"
    content_tree = {current_heading: []}
    for line in page_content.split('\n'):
        if line:
            is_heading, heading = _parse_heading(line)
            if is_heading:
                current_heading = heading
                content_tree[current_heading] = []
            else:
                content_tree[current_heading].append(line)
    logger.debug(pprint.pformat(content_tree))
    return content_tree


def _parse_content_flat(page_content):
    content_flat = []
    tree = _parse_content_tree(page_content)
    skip_sections = {
        "None",
        "== External links ==",
        "== Further reading ==",
        "== Notes ==",
        "== References ==",
        "== See also =="
    }

    for title, section in tree.items():
        if title not in skip_sections:
            content_flat.extend(section)

    return content_flat


def get_random_page():
    # https://wikipedia.readthedocs.org/en/latest/quickstart.html
    random_title = wikipedia.random(pages=1)
    random_page = None
    while not random_page:
        try:
            random_page = wikipedia.page(title=random_title)
        except wikipedia.PageError:
            random_title = wikipedia.random(pages=1)
            random_page = None
        except wikipedia.DisambiguationError as e:
            random_title = random.choice(e.options)
            random_page = None
    return random_page


logger = logging.getLogger(__name__)

misconceptions = _parse_content_flat(wikipedia.page("List of common misconceptions").content)
python_facts = _parse_content_flat(wikipedia.page("Python (programming language)").content)


def get_random_misconception():
    return random.choice(misconceptions)


def get_random_python_fact():
    return random.choice(python_facts)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    for i in range(3):
        print(random.choice(python_facts))


def get_all_misconceptions():
    return misconceptions