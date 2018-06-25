import sys


def clean_string(dirty):
    if dirty:
        encoded = dirty.encode(sys.stdout.encoding, errors='replace')
        return encoded.decode(sys.stdout.encoding)
    else:
        return None
