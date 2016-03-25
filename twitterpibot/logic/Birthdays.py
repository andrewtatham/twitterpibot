import datetime

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


def get_birthday_users(today=None):
    if not today:
        today = datetime.date.today().strftime("%d/%m")
    if today in _birthdays:
        return _birthdays[today]
    else:
        return None
