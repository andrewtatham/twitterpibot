import pprint
from unittest import TestCase
import flask
from twitterpibot.ui.Controller import Controller

__author__ = 'andrewtatham'


class TestController(TestCase):
    def test_get_identities(self):

        print(flask.json.dumps({}))
        print(flask.json.dumps(list({1,2,3})))
        print(flask.json.dumps(list({"a","b","c"})))



        controller = Controller()
        actual = controller.get_identities()
        pprint.pprint(actual)
        self.fail()


