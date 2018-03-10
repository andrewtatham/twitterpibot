def circly_upper(text):
    return "".join(map(add(9333), text.upper()))


def circly_lower(text):
    return "".join(map(add(9359), text.upper()))


def script_bold(text):
    return "".join(map(add(119951), text.upper()))


def fraktur_bold(text):
    return "".join(map(add(120107), text.upper()))


def monospace(text):
    return "".join(map(add(120367), text.upper()))


def add(n):
    return lambda c: " " if c == " " else chr(n + ord(c))


def uppercase_spaced(text):
    return " ".join(text.upper())


if __name__ == '__main__':
    blah = "BLAH Blah blah"
    mutated = monospace(blah)
    print(mutated)
