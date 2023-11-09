"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.dfa import DeterministicFiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism


class TestMinimize(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_minimize(self, automaton, simplified):
        """Test that the minimized automaton is the simplified one."""
        minimized = DeterministicFiniteAutomaton.to_minimized(automaton)
        equiv_map = deterministic_automata_isomorphism(minimized, simplified)

        self.assertTrue(equiv_map is not None)
    
    
    def test_empty_language(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: a

            Initial
            NotReached1
            NotReached2
            Empty

            ini Initial -a-> Empty
            NotReached1 -a-> NotReached2
            NotReached2 -a-> Empty
            Empty -a-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: a

            Initial

            ini Initial -a-> Initial
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)

    def test_empty_str_language(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: a

            Initial final
            NotReached1
            NotReached2
            Empty

            ini Initial -a-> Empty
            NotReached1 -a-> NotReached2
            NotReached2 -a-> Empty
            Empty -a-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: a

            Initial final
            Empty 

            ini Initial -a-> Empty
            Empty -a-> Empty
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)

    def test_redundant_states(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: ab

            Initial
            B1 final
            B2 final
            Empty

            ini Initial -a-> B1
            Initial -b-> Empty
            B1 -a-> B1
            B1 -b-> B2
            B2 -a-> B1
            B2 -b-> B1
            Empty -a-> Empty
            Empty -b-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: ab

            Initial
            B final
            Empty

            ini Initial -a-> B
            Initial -b-> Empty
            B -a-> B
            B -b-> B
            Empty -a-> Empty
            Empty -b-> Empty
        """

        simplified = AutomataFormat.read(simplified_str).to_deterministic()

        self._check_minimize(automaton, simplified)

    def test_minimization_presentation(self):
        """Test the automaton from the minimization presentation."""
        automaton_str = """
        Automaton:
            Symbols: 01

            A
            B
            C final
            D
            E
            F
            G
            H

            ini A -0-> B
            A -1-> F
            B -0-> G
            B -1-> C
            C -0-> A
            C -1-> C
            D -0-> C
            D -1-> G
            E -0-> H
            E -1-> F
            F -0-> C
            F -1-> G
            G -0-> G
            G -1-> E
            H -0-> G
            H -1-> C
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: 01

            AE
            BH
            F
            G
            C final 

            ini AE -0-> BH
            AE -1-> F
            BH -0-> G
            BH -1-> C
            F -0-> C
            F -1-> G
            G -0-> G
            G -1-> AE
            C -0-> AE
            C -1-> C
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)


    
if __name__ == '__main__':
    unittest.main()
