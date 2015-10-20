
import Songs
import datetime

_songs = Songs.Songs()
_birthdays = {
        "02/01" : ["andrewtatham"],
        "21/10" : ["fuuuunnnkkytree"],
        "17/03" : ["sheriffredleg"],
        "20/05" : ["morris_helen"],
        "20/10" : ["andrewtathampi2"]
    }

def GetBirthdayUsers():
    today = datetime.date.today().strftime("%d/%m")

    if today in _birthdays:
        return _birthdays[today]
    else:
        return None

def SingBirthdaySong(screen_name):
    _songs.SingBirthdaySong(screen_name)