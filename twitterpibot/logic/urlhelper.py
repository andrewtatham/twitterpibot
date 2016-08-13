import base64
import hashlib
import hmac
import json
import logging
import pprint
import re
from urllib.parse import urlparse

import requests

from twitterpibot.exceptionmanager import handle

__author__ = 'andrewtatham'

logger = logging.getLogger(__name__)


def parameterise(params, url):
    first = True
    for param in params:
        if first:
            url += "?"
            first = False
        else:
            url += "&"
        url += param + "={" + param + "}"
    # for param in params:
    #     params[param] = quote_plus(str(params[param]).encode())
    url = url.format(**params)
    return url


def _sign_url(input_url, secret):
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


def parameters_and_sign(params, url, secret):
    url = parameterise(params, url)
    url = _sign_url(input_url=url, secret=secret)
    logger.info("URL: " + url)
    return url


def get_response(url):
    response_dict = None
    try:
        logger.info(url)
        response = requests.get(url)
        logger.info(response)
        response.raise_for_status()
        response_json = response.content.decode()
        response_dict = json.loads(response_json)
        logger.debug(pprint.pformat(response_dict))
    except requests.exceptions.HTTPError as ex:
        handle(None, ex, url)

    return response_dict


url_rx = re.compile("(https?://(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})", re.IGNORECASE)


def extract_urls(text):
    urls = []
    if text:
        matches = url_rx.findall(text)
        if matches:
            urls.extend(matches)
    return urls


def count_urls(text):
    if text:
        return len(extract_urls(text))
    else:
        return 0


if __name__ == '__main__':
    text = "@blah RT Blah http://link1.com/abc.html, http://link2.co.uk/abc?xyz=%20"
    pprint.pprint(extract_urls(text))
