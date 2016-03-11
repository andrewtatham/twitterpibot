import datetime
import os
import pprint
import hashlib
import hmac
import base64
from urllib.parse import urlparse

import googlemaps

from twitterpibot.logic import fsh

key = fsh.get_key("google")
secret = fsh._get("secret", "google")


def _sign_url(input_url=None, secret=None):
    """ Sign a request URL with a URL signing secret.

        Usage:
        from urlsigner import sign_url

        signed_url = sign_url(input_url=my_url, secret=SECRET)

        Args:
        input_url - The URL to sign
        secret    - Your URL signing secret

        Returns:
        The signed request URL
    """
    # https://developers.google.com/maps/documentation/streetview/get-api-key#dig-sig-key

    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    input_url = input_url.encode()
    secret = secret.encode()

    url = urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + b"?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, url_to_sign, hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + b"://" + url.netloc + url.path + b"?" + url.query

    # Return signed URL
    encoded_signed_bytes = original_url + b"&signature=" + encoded_signature
    return encoded_signed_bytes.decode()


def api():
    gmaps = googlemaps.Client(key=key)

    # Geocoding an address
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    pprint.pprint(geocode_result)

    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    pprint.pprint(reverse_geocode_result)

    # Request directions via public transit
    now = datetime.datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)

    pprint.pprint(directions_result)


def get_streetview_image():
    global key
    # https://developers.google.com/maps/documentation/streetview/intro#url_parameters
    params = {
        "location": "41.403609,2.174448",
        "fov": 90,  # min ? def 90 max 120
        "heading": 360 - 30,  # 0-360
        "pitch": 45  # down -90 def 0 up 90
    }
    if "size" not in params:
        params["size"] = "640x640"
        params["size"] = "640x480"
        # params["size"] = "456x456"
    if "key" not in params:
        params["key"] = key
    url = "https://maps.googleapis.com/maps/api/streetview"
    first = True
    for key in params:
        if first:
            url += "?"
            first = False
        else:
            url += "&"
        url += key + "={" + key + "}"
    print(url)
    url = url.format(**params)
    print(url)
    signed = _sign_url(input_url=url, secret=secret)
    print("Signed URL: " + signed)
    folder = fsh.root + "temp" + os.sep + "images" + os.sep + "google" + os.sep
    file_path = fsh.download_file(folder=folder, url=url, file_name="streetview.jpg")
    print(file_path)
    return file_path


if __name__ == "__main__":
    get_streetview_image()
