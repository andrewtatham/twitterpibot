import datetime


def is_christmas(today=None):
    if not today:
        today = datetime.date.today()
    return today.month == 12 and 24 <= today.day <= 26
