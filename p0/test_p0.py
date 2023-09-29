#!/usr/bin/env python

import re
import unittest

from regular_expressions import RE0, RE1, RE2, RE3, RE4, RE5, RE6


class TestP0(unittest.TestCase):
    """Tests of assignment 0."""

    def check_expression(self, expr: str, string: str, expected: bool) -> None:
        with self.subTest(string=string):
            match = re.fullmatch(expr, string)
            self.assertEqual(bool(match), expected)

    def test_exercise_0(self) -> None:
        self.check_expression(RE0, "a", True)
        self.check_expression(RE0, "bbbbaba", True)
        self.check_expression(RE0, "abbab", False)
        self.check_expression(RE0, "b", False)

    def test_exercise_1(self) -> None:
        self.check_expression(RE1, "a", True)
        self.check_expression(RE1, "b", True)
        self.check_expression(RE1, "ab", True)
        self.check_expression(RE1, "aab", True)
        self.check_expression(RE1, "abbb", True)

        self.check_expression(RE1, "ba", False)
        self.check_expression(RE1, "bba", False)
        self.check_expression(RE1, "aba", False)
        self.check_expression(RE1, "aaba", False)


    def test_exercise_2(self) -> None:
        self.check_expression(RE2, "a", True)
        self.check_expression(RE2, "ab", True)
        self.check_expression(RE2, "aba", True)
        self.check_expression(RE2, "abababa", True)
        self.check_expression(RE2, "abababab", True)
        self.check_expression(RE2, "ababababa", True)
        self.check_expression(RE2, "ababababab", True)
        self.check_expression(RE2, "ba", True)
        self.check_expression(RE2, "bab", True)
        self.check_expression(RE2, "babababa", True)
        self.check_expression(RE2, "babababab", True)
        self.check_expression(RE2, "bababababa", True)
        self.check_expression(RE2, "bababababab", True)

        self.check_expression(RE2, "aa", False)
        self.check_expression(RE2, "aab", False)
        self.check_expression(RE2, "aabaa", False)
        self.check_expression(RE2, "aabaab", False)
        self.check_expression(RE2, "bb", False)
        self.check_expression(RE2, "bbababb", False)
        self.check_expression(RE2, "aaa", False)
        self.check_expression(RE2, "abaabb", False)
        self.check_expression(RE2, "ababbab", False)
        self.check_expression(RE2, "bababbab", False)
        self.check_expression(RE2, "abaaba", False)
        self.check_expression(RE2, "babaaba", False)


    def test_exercise_3(self) -> None:
        self.check_expression(RE3, "aabb", True)
        self.check_expression(RE3, "abbaa", True)
        self.check_expression(RE3, "aaabaabababbaab", True)
        self.check_expression(RE3, "abbbbaabababbaab", True)
        self.check_expression(RE3, "abbbbbababbaab", True)
        self.check_expression(RE3, "abbbbbaaab", True)

        self.check_expression(RE3, "ababaa", False)
        self.check_expression(RE3, "aaaaaaaaab", False)
        self.check_expression(RE3, "bbbbbbbbba", False)
        self.check_expression(RE3, "aaaaaaaaa", False)
        self.check_expression(RE3, "bbbbbbb", False)
        self.check_expression(RE3, "b", False)
        self.check_expression(RE3, "a", False)
        self.check_expression(RE3, "abbabb", False)
        self.check_expression(RE3, "aabab", False)
        self.check_expression(RE3, "aababa", False)
        self.check_expression(RE3, "aababaa", False)
        self.check_expression(RE3, "bbabab", False)
        self.check_expression(RE3, "bbaba", False)

    def test_exercise_4(self) -> None:
        self.check_expression(RE4, "0", True)
        self.check_expression(RE4, "10", True)
        self.check_expression(RE4, "22", True)
        self.check_expression(RE4, "190", True)
        self.check_expression(RE4, "250", True)
        self.check_expression(RE4, "130", True)
        self.check_expression(RE4, "1", True)
        self.check_expression(RE4, "8", True)
        self.check_expression(RE4, "18", True)
        self.check_expression(RE4, "255", True)

        self.check_expression(RE4, "-1", False)
        self.check_expression(RE4, "+1", False)
        self.check_expression(RE4, "007", False)
        self.check_expression(RE4, "017", False)
        self.check_expression(RE4, "07", False)
        self.check_expression(RE4, "3.33", False)
        self.check_expression(RE4, "256", False)


    def test_exercise_5(self) -> None:
        self.check_expression(RE5, "a", True)
        self.check_expression(RE5, "aa", True)
        self.check_expression(RE5, "abaa", True)
        self.check_expression(RE5, "baa", True)
        self.check_expression(RE5, "baabbbbba", True)
        self.check_expression(RE5, "baabbbbba", True)
        self.check_expression(RE5, "bbbbbabbbbbaa", True)
        self.check_expression(RE5, "bbbbbaabbbbbaa", True)
        self.check_expression(RE5, "babababaa", True)
        self.check_expression(RE5, "babaababaa", True)
        self.check_expression(RE5, "babababaaa", True)
        self.check_expression(RE5, "aabbbbbbbbbb", True)
        self.check_expression(RE5, "aabbbbbbbbbba", True)
        self.check_expression(RE5, "aababababab", True)
        self.check_expression(RE5, "ababaababab", True)

        self.check_expression(RE5, "aabaaaa", False)
        self.check_expression(RE5, "baababaabababaa", False)
        self.check_expression(RE5, "aabababaabababaa", False)
        self.check_expression(RE5, "bbaabaabaaaa", False)
        self.check_expression(RE5, "bbaaaabaabaaaa", False)
        self.check_expression(RE5, "bbbbbbaaaaaa", False)
        self.check_expression(RE5, "aabbbbbbaaaaaa", False)
        self.check_expression(RE5, "aabbbbbbaabbbbbbaa", False)
        self.check_expression(RE5, "aabbbbbbaabababaaa", False)
        self.check_expression(RE5, "aabababaaabbbbbbaabbbbbbaa", False)

    def test_exercise_6(self) -> None:
        self.check_expression(RE6, "1", True)
        self.check_expression(RE6, "0", True)
        self.check_expression(RE6, "0011", True)

        self.check_expression(RE6, "0000", False)
        self.check_expression(RE6, "1111", False)


if __name__ == '__main__':
    unittest.main()
