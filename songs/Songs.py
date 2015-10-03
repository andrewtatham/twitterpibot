class Songs(object):
    def __init__(self, *args, **kwargs):

        self.songs = CaseInsensitiveDict(
            {
            "500miles": {
                "artist" : "",
                "screen_name" : "@The_Proclaimers",
                "title": "",
                "lyrics": "500miles.txt",
                "video": "https://youtu.be/tM0sTNtWDiI"
            },
            "dontstopbelieving": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "believin.txt",
                "video": "https://youtu.be/KCy7lLQwToI"
            },
            "surfinbird": {
                "artist" : "",
                "screen_name" : "",
                "title": "",
                "lyrics": "bird.txt",
                "video": "https://youtu.be/9Gc4QTqslN4"
            },
            "bluemonday": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "bluemonday.txt",
                "video": "https://youtu.be/FYH8DsU2WCk"
            },
            "bohrap": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "bohrap.txt",
                "video": "https://youtu.be/fJ9rUzIMcZQ"
            },
            "boomshackalack": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "boomshackalack.txt",
                "video": "https://youtu.be/kZzBd41NuZw"
            },
            "commonpeople": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "common.txt",
                "video": "https://youtu.be/yuTMWgOduFM"
            },
            "compton": {
                "artist" : "N.W.A.",
                "screen_name" : "@mcrencpt @icecube @drdre",
                "title": "",
                "lyrics": "compton.txt",
                "video": "https://youtu.be/TMZi25Pq3T8"

            },
            ##"dodgeball": {
            ##    "artist" : "",
            ##    "title": "",
            ##    "lyrics": "dodgeball.txt",
            ##    "video": ""
            ##},
            "forgotaboutdre": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "forgot.txt",
                "video": "https://youtu.be/QFcv5Ma8u8k"
            },
            "freshprince": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "freshprince.txt",
                "video": "https://youtu.be/hBe0VCso0qs"
            },
            "gangstersparadise": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "gangsters.txt",
                "video": "https://youtu.be/cpGbzYlnz7c"
            },
            "icebaby": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "ice.txt",
                "video": "https://youtu.be/rog8ou-ZepE"
            },
            "incredible": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "incredible.txt",
                "video": "https://youtu.be/mL2Bgj-za5k"
            },
            "informer": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "informer.txt",
                "video": "https://youtu.be/StlMdNcvCJo"
            },
            "japanese": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "japanese.txt",
                "video": "https://youtu.be/mgekmOqCFTU"
            },
            "jinglebells": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "jingle.txt",
                "video": "https://youtu.be/FVJskPa2a3s"
            },
            "welcometothejungle": {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title": "",
                "lyrics": "jungle.txt",
                "video": "https://youtu.be/o1tj2zJ2Wvg"
            },
            "nighttrain": {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title": "",
                "lyrics": "nighttrain.txt",
                "video": "https://youtu.be/Qyf8oRF6Trg"
            },
            "novemberrain": {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title": "",
                "lyrics": "novemberrain.txt",
                "video": "https://youtu.be/8SbUC-UaAxE"
            },
            "paradisecity": {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title": "",
                "lyrics": "paradise.txt",
                "video": "https://youtu.be/Rbm6GXllBiw"
            },
            "fuckthepolice": {
                "artist" : "N.W.A.",
                "screen_name" : "@mcrencpt @icecube @drdre",
                "title": "",
                "lyrics": "police.txt",
                "video": "https://youtu.be/Z7-TTWgiYL4"
            },
            "rickroll": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "rickroll.txt",
                "video": "https://youtu.be/dQw4w9WgXcQ"
            },
            "rocklobster": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "rocklobster.txt",
                "video": "https://youtu.be/tDZy6-fMCw4"
            },
            "toosexy": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "sexy.txt",
                "video": "https://youtu.be/YFmsgHfuXpA"
            },
            "spinmeround": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "spinmeround.txt",
                "video": "https://youtu.be/PGNiXGX2nLU"
            },
            "stilldre": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "stilldre.txt",
                "video": "https://youtu.be/_CL6n0FJZpk"
            },
            "stuckinthemiddle": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "stuckinthemiddle.txt",
                "video": "https://youtu.be/DohRa9lsx0Q"
            },
            "sweetchildomine": {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title": "",
                "lyrics": "sweet.txt",
                "video": "https://youtu.be/1w7OgIMMRc4"
            },
            "wonderwall": {
                "artist" : "",
                "screen_name" : None,
                "title": "",
                "lyrics": "wonderwall.txt",
                "video": "https://youtu.be/6hzrDeceEKc"
            }
        }
    )
        



class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())