import datetime
import re


def _init_regex(regular_expression_list):
    def make_spaces_optional(rx):
        return rx.replace(" ", " ?")

    return re.compile("|".join(map(make_spaces_optional, regular_expression_list)), re.IGNORECASE)


class Topic(object):
    def __init__(self,
                 definite_regexes,
                 possible_regexes=None,
                 from_date=None,
                 to_date=None,
                 on_date=None,
                 on_date_range=0,
                 retweet=False):

        self._retweet = retweet

        self._definite_rx = _init_regex(definite_regexes)
        self._possible_rx = None
        if possible_regexes:
            self._possible_rx = _init_regex(possible_regexes)

        self._init_date_range(from_date, to_date, on_date, on_date_range)

    def _init_date_range(self, from_date, to_date, on_date, on_date_range):
        self._from_date = None
        self._from_month = None
        self._to_date = None
        self._to_month = None

        if on_date and on_date_range:
            parts = on_date.split("/")
            dt = datetime.date(
                year=datetime.date.today().year,
                month=int(parts[1]),
                day=int(parts[0]))
            delta = datetime.timedelta(days=on_date_range)
            frm = dt - delta
            to = dt + delta
            self._from_date = frm.day
            self._from_month = frm.month
            self._to_date = to.day
            self._to_month = to.month
        if from_date:
            parts = from_date.split("/")
            self._from_date = int(parts[0])
            self._from_month = int(parts[1])
        if to_date:
            parts = to_date.split("/")
            self._to_date = int(parts[0])
            self._to_month = int(parts[1])

    def condition(self, text, today=None):

        result = {'topic': self.__class__.__name__}

        has_date_range = self._from_date and self._from_month and self._to_date and self._to_month

        is_date_match = False

        if has_date_range:
            if not today:
                today = datetime.date.today()

            is_date_match = self._from_date <= today.day <= self._to_date \
                            and self._from_month <= today.month <= self._to_month

        if not has_date_range or is_date_match:
            definite_matches = list(self._definite_rx.findall(text))
            if definite_matches:
                result["definite_matches"] = definite_matches
                return result
            elif self._possible_rx:
                possible_matches = list(self._possible_rx.findall(text))
                if possible_matches:
                    result["possible_matches"] = possible_matches
                    return result
                else:
                    return None
        else:
            return None

    def retweet(self):
        return self._retweet

    def __str__(self):
        return self.__class__.__name__
