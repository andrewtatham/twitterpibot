from twitterpibot.songs.Songs import Songs
import datetime

_songs = Songs()
_birthdays = {
    "02/01": ["andrewtatham"],
    "17/03": ["sheriffredleg", "JamesDawg"],
    "20/05": ["morris_helen"],
    "10/06": ["dcspamoni", "stevensenior"],
    "22/06": ["jami3rez"],
    "23/07": ["Tolle_Lege"],
    "28/08": ["Chariteee"],
    "21/09": ["hippypottermice"],
    "09/10": ["paulfletcher79"],
    "20/10": ["andrewtathampi2"],
    "22/10": ["fuuuunnnkkytree"],
}


def get_birthday_users():
    today = datetime.date.today().strftime("%d/%m")

    if today in _birthdays:
        return _birthdays[today]
    else:
        return None


def sing_birthday_song(identity, screen_name):
    _songs.sing_birthday_song(identity, screen_name)
