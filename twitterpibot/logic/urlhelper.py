__author__ = 'andrewtatham'


def url_paramaters(params, url):
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
