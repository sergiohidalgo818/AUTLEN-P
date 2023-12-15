import unittest
from typing import AbstractSet

from grammar.grammar import Grammar
from grammar.utils import GrammarFormat


class TestFollow(unittest.TestCase):
    def _check_follow(
        self,
        grammar: Grammar,
        symbol: str,
        follow_set: AbstractSet[str],
    ) -> None:
        with self.subTest(string=f"Follow({symbol}), expected {follow_set}"):
            computed_follow = grammar.compute_follow(symbol)
            self.assertEqual(computed_follow, follow_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "E", {'$', ')'})
        self._check_follow(grammar, "T", {'$', ')', '+'})
        self._check_follow(grammar, "X", {'$', ')'})
        self._check_follow(grammar, "Y", {'$', ')', '+'})

    def test_case2(self) -> None:
        """Test Case 2."""
        grammar_str = """
        X -> I*AD
        I -> A*I
        I -> a
        I ->
        A -> aa*A
        A -> a
        A ->
        Y -> *T
        D -> *
        D ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "A", {'$', '*'})
        self._check_follow(grammar, "D", {'$'})
        self._check_follow(grammar, "I", {'*'})
        self._check_follow(grammar, "X", {'$'})

    def test_case3(self) -> None:
        """Test Case 3."""
        grammar_str = """
        A -> BCD
        B -> <
        B ->
        C -> 0C;
        C -> 1C;
        D -> 0>
        D -> 1>
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "A", {'$'})
        self._check_follow(grammar, "B", {'1', '0'})
        self._check_follow(grammar, "C", {'1', '0', ';'})
        self._check_follow(grammar, "D", {'$'})
    
if __name__ == '__main__':
    unittest.main()
