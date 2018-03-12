import logging
from unittest import TestCase

from twitterpibot.logic import unicode_helper, emojihelper

testcases = [
    # 730100 seitsemänsataakolmekymmentätuhattasata


    {
        "text": """""",
        "expected": None
    },
    {
        "text": "Blah, blah, & blah.",
        "expected": unicode_helper.LatinText
    },
    {
        "text": "730104 seitsemänsataakolmekymmentätuhattasataneljä",
        "expected": unicode_helper.LatinText
    },

    {
        "text": "(48, 72)(288, 88)(248, 146)(84, 256)  # notasquare",
        "expected": unicode_helper.NumericText
    },
    {
        "text": "" + emojihelper.white_smiling_face,
        "expected": unicode_helper.UnicodeArt
    },

    {
        "text": """
            乀❧ɽ❃ᢇា឵឴✾❊❊⇮ജ🌸ణ❋⨌⚜
            ❉ʃ❦⚘丿❊✿🌺⇞❊✢ა❃⚲Ⴔ
              ₹𝟠❧⇂❁ಣ💐∫✾❀❈❊ⷘლɾ
            ₸ㅏ🌳𝟠⁕ణ⚜Ì✿〡✥❁↟ణ✤
            ❃↓ɾ❈〃ლ❁ノ∬❧✥❋lლ✥
              ✢✥║❃⨌✤𝟠⁕❧ത❁✻ლ✼ⷞ
            յ₹𝟠ℌ❁亅ლ✢𝟠❈✿⚘↶₸❊
             乀⚜🍀ƪ✥🌱✢❧ⶫಣ⚘↷ƪ丿ణ
        """,
        "expected": unicode_helper.UnicodeArt
    },

    {
        "text": """
            ∴∥∴
            　　　　　∴＼∨／∴
            　＊│＊　＝＞☏＜＝
            ＊＼※／＊∵／∧＼∵
            ─※☎※─　∵∥∵
            ＊／※＼＊ ・
            　＊│＊　
            ┈┈┈┈▅┈┈▕■┈┈┈┈┈
            ┈┈┈▕┈┈┈╱╲▕■┈┈
            ┈┈┈╱╲┈┈▏▕╱╲┈
            ┈┈┈▏▕╱╲▏▎▏▕╱╲┈▃ #telephone
        """,
        "expected": unicode_helper.UnicodeArt
    },

    {
        "text": """
            ┌──┬┬─🍔
            ├├─┼┘┤┤
            ├┤┤┐└┤┤
            ├┌┐┴┐└┤
            ├──┴─┴┤
            ├─┤┘┴├┤
            ├─┐┤─┘┤
            ├──┘┴┤┤
            ├┤┤┘├├┤
            ├──┬─┌┤
            ├┬┐─┴┬┤
            ├┤├┘┬┬┤
            ├─┌┤┌┤┤
            ├┤┌┤┤┘┤
            ├─├┌┐┬┤
            ├┴┘┐├─┤
            └┴──┴─🐁
        """,
        "expected": unicode_helper.UnicodeArt
    },

    {
        "text": """
            掲示板建てておきますね
            　＿＿＿＿＿＿＿＿＿_
            ∠＿＿＿＿＿＿＿＿＿△
            　|　 ○○町内会 |:｜
            　|―――――――|:｜
            　|　　　　　　　|:｜
            　|　　　　　　　|:｜
            　|　　　　　　　|:｜
            　|＿＿＿＿＿＿＿|:｜
            　|:｜　　　　　 |:｜
        """,
        "expected": unicode_helper.UnicodeArt
    },

]


class TestAnalyse(TestCase):
    def test_analyse(self):
        logging.basicConfig(level=logging.DEBUG)
        for testcase in testcases:
            with self.subTest(testcase):
                actual = unicode_helper.analyse(testcase["text"])
                expected_type = testcase["expected"]
                if expected_type:
                    self.assertIsInstance(actual, expected_type)
                else:
                    self.assertIsNone(actual)
