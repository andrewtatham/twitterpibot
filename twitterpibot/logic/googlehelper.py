import json
import logging
import os
import hashlib
import hmac
import base64
import pprint
import random
from urllib.parse import urlparse, quote_plus

import requests

from twitterpibot import dal
from twitterpibot.logic import fsh, urlhelper

logger = logging.getLogger(__name__)

key = dal.get_token("google api")
secret = dal.get_token("google secret").encode()
custom_search_id = dal.get_token("google cse")

folder = fsh.root + "temp" + os.sep + "images" + os.sep + "google" + os.sep


def _sign_url(input_url=None):
    # https://developers.google.com/maps/documentation/streetview/get-api-key#dig-sig-key

    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    input_url = input_url.encode()

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


def _urlbuild(params, url, sign=True):
    url = urlhelper.url_paramaters(params, url)
    if sign:
        url = _sign_url(input_url=url)
    logger.info("URL: " + url)
    return url


def _get_url(url):
    response = requests.get(url)
    response_json = response.content.decode()
    response_dict = json.loads(response_json)
    logger.info(pprint.pformat(response_dict))
    return response_dict


def get_streetview_image(location, heading, pitch=0, fov=90):
    # https://developers.google.com/maps/documentation/streetview/intro#url_parameters
    params = {
        'location': location.get_latlng_param(),
        'fov': fov,
        'heading': heading,
        'pitch': pitch,
        "size": "640x480",
        "key": key}

    return _urlbuild(params, "https://maps.googleapis.com/maps/api/streetview")


def get_map_image(location, zoom):
    # https://developers.google.com/maps/documentation/static-maps/intro#URL_Parameters
    params = {
        "center": location.get_address_param(),
        "zoom": zoom,
        "maptype": "hybrid",
        "size": "640x480",
        "key": key}
    return _urlbuild(params, "https://maps.googleapis.com/maps/api/staticmap")


def get_search_images(text, number):
    params = {
        "q": quote_plus(text),
        "searchType": "image",
        "num": number,
        "cx": custom_search_id,
        "key": key
    }

    url = _urlbuild(params, "https://www.googleapis.com/customsearch/v1")
    response = _get_url(url)
    urls = [item["link"] for item in response["items"]]
    return urls


def get_location_images(location, name):
    urls = []
    for zoom in [12]:
        urls.append(get_map_image(location, zoom=zoom))

    urls.extend(get_search_images(location.get_address_param(), 1))

    heading = random.randint(0, 360)
    for bearing in [0]:
        urls.append(get_streetview_image(
            location,
            heading=(heading + bearing) % 360,
            fov=120))

    i = 0
    file_paths = []
    for url in urls:
        file_name = name + str(i) + ".jpg"
        file_paths.append(fsh.download_file(folder=folder, url=url, file_name=file_name))
        i += 1


def geocode(location):
    # https://developers.google.com/maps/documentation/geocoding/intro#geocoding
    params = {
        "address": location.get_address_param(),
        "key": key}
    url = _urlbuild(params, "https://maps.googleapis.com/maps/api/geocode/json", sign=False)
    response_dict = _get_url(url)
    if response_dict["status"] != "ZERO_RESULTS" and response_dict["results"]:
        location.latitude = response_dict["results"][0]["geometry"]["location"]["lat"]
        location.longitude = response_dict["results"][0]["geometry"]["location"]["lng"]
        return location
    else:
        return None


def reverse_geocode(location):
    # https://developers.google.com/maps/documentation/geocoding/intro#ReverseGeocoding
    params = {
        "latlng": location.get_latlng_param(),
        "key": key}
    url = _urlbuild(params, "https://maps.googleapis.com/maps/api/geocode/json", sign=False)
    response_dict = _get_url(url)
    if response_dict["status"] != "ZERO_RESULTS" and response_dict["results"]:
        location.full_name = response_dict["results"][0]["formatted_address"]
        logger.info(location.full_name)
        return location
    else:
        return None


if __name__ == "__main__":
    from twitterpibot.logic import location
    # loc = location.Location(latitude=41.403609, longitude=2.174448)  # La Sagrada Familia
    # loc = location.Location(latitude=40.714224, longitude=-73.961452)  # Grand St/Bedford Av, Brooklyn, NY 11211, USA
    # loc = location.get_random_location_by_latlng()
    # loc = reverse_geocode(loc)
    # get_location_images(loc, "reverse_geocode")

    loc = location.get_random_location_by_name()
    loc = geocode(loc)
    get_location_images(loc, "geocode")
