import datetime
import re
import logging

logger = logging.getLogger(__name__)


def _init_regex(regular_expression_list):
    def make_spaces_optional(rx):
        return r"\b" + rx.replace(" ", r" ?") + r"\b"

    regex = "|".join(map(make_spaces_optional, regular_expression_list))
    logger.debug(regex)
    return re.compile(regex, re.IGNORECASE)


class Topic(object):
    def __init__(self,
                 definite_regexes,
                 possible_regexes=None,
                 from_date=None,
                 to_date=None,
                 on_date=None,
                 on_date_range=0,
                 retweet=False,
                 reply=False,
                 stream=False,
                 spam=False,
                 score=0,
                 except_regexes=None
                 ):

        self._retweet = retweet
        self._reply = reply
        self._stream = stream
        self._spam = spam
        self._score = score

        self.definite_rx = _init_regex(definite_regexes)

        self.possible_rx = None
        if possible_regexes:
            self.possible_rx = _init_regex(possible_regexes)

        self.except_rx = None
        if except_regexes:
            self.except_rx = _init_regex(except_regexes)

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

    def reply(self):
        return self._reply

    def retweet(self):
        return self._retweet

    def spam(self):
        return self._spam

    def condition(self, text, today=None):

        result = {
            'topic': self.__class__.__name__,
            'retweet': self.retweet(),
            'reply': self.reply(),
            'stream': self._stream,
            'spam': self.spam(),
            'score': self._score
        }

        has_date_range = self._from_date and self._from_month and self._to_date and self._to_month

        is_date_match = False

        if has_date_range:
            if not today:
                today = datetime.date.today()

            is_date_match = self._from_date <= today.day <= self._to_date \
                            and self._from_month <= today.month <= self._to_month

        if not has_date_range or is_date_match:
            except_matches = None
            if self.except_rx:
                except_matches = [match.group(0) for match in self.except_rx.finditer(text) if match]
            if not except_matches:
                definite_matches = [match.group(0) for match in self.definite_rx.finditer(text) if match]
                if definite_matches:
                    result["definite_matches"] = definite_matches
                    return result
                elif self.possible_rx:
                    possible_matches = [match.group(0) for match in self.possible_rx.finditer(text) if match]
                    if possible_matches:
                        result["possible_matches"] = possible_matches
                        return result


class GoodTopic(Topic):
    def __init__(self,
                 definite_regexes,
                 possible_regexes=None,
                 from_date=None,
                 to_date=None,
                 on_date=None,
                 on_date_range=0,
                 except_regexes=None
                 ):
        super(GoodTopic, self).__init__(
            definite_regexes,
            possible_regexes,
            from_date,
            to_date,
            on_date,
            on_date_range,
            retweet=True,
            reply=True,
            stream=True,
            score=2,
            except_regexes=except_regexes)


class IgnoreTopic(Topic):
    def __init__(self,
                 definite_regexes,
                 possible_regexes=None,
                 from_date=None,
                 to_date=None,
                 on_date=None,
                 on_date_range=0,
                 except_regexes=None
                 ):
        super(IgnoreTopic, self).__init__(
            definite_regexes,
            possible_regexes,
            from_date,
            to_date,
            on_date,
            on_date_range,
            retweet=False,
            reply=False,
            stream=False,
            score=-1,
            except_regexes=except_regexes)


class NewsTopic(Topic):
    def __init__(self,
                 definite_regexes,
                 possible_regexes=None,
                 from_date=None,
                 to_date=None,
                 on_date=None,
                 on_date_range=0,
                 except_regexes=None
                 ):
        super(NewsTopic, self).__init__(
            definite_regexes,
            possible_regexes,
            from_date,
            to_date,
            on_date,
            on_date_range,
            retweet=True,
            reply=False,
            stream=True,
            score=0,
            except_regexes=except_regexes)


class BadTopic(Topic):
    def __init__(self,
                 definite_regexes,
                 possible_regexes=None,
                 from_date=None,
                 to_date=None,
                 on_date=None,
                 on_date_range=0,
                 except_regexes=None
                 ):
        super(BadTopic, self).__init__(
            definite_regexes,
            possible_regexes,
            from_date,
            to_date,
            on_date,
            on_date_range,
            retweet=False,
            reply=False,
            stream=False,
            spam=False,
            score=-1,
            except_regexes=except_regexes)


class SpamTopic(Topic):
    def __init__(self,
                 definite_regexes,
                 possible_regexes=None,
                 from_date=None,
                 to_date=None,
                 on_date=None,
                 on_date_range=0,
                 except_regexes=None
                 ):
        super(SpamTopic, self).__init__(
            definite_regexes,
            possible_regexes,
            from_date,
            to_date,
            on_date,
            on_date_range,
            retweet=False,
            reply=False,
            stream=False,
            spam=True,
            score=-5,
            except_regexes=except_regexes)
