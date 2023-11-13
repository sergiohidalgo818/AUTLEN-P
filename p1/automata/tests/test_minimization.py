"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.dfa import DeterministicFiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot


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

        w = '''Test empty lenguage:\n\nRecived:\n'''

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(DeterministicFiniteAutomaton.to_minimized(automaton))
        w += '''\n\n'''

        f = open("tests_data/tests_minimization.txt", "w")
        f.write(w)
        f.close()

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

        w = '''Test empty str:\n\nRecived:\n'''

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(DeterministicFiniteAutomaton.to_minimized(automaton))
        w += '''\n\n'''

        f = open("tests_data/tests_minimization.txt", "a")
        f.write(w)
        f.close()

    def test_redundant_states(self):
        """Test an automaton redundant state."""
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

        w = '''Test redundant states:\n\nRecived:\n'''

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(DeterministicFiniteAutomaton.to_minimized(automaton))
        w += '''\n\n'''

        f = open("tests_data/tests_minimization.txt", "a")
        f.write(w)
        f.close()

    def test_minimization_presentation(self):
        """Test the automaton from the minimization presentation. (guide)"""
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

        w = '''Test from presentation:\n\nRecived:\n'''

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(DeterministicFiniteAutomaton.to_minimized(automaton))
        w += '''\n\n'''

        f = open("tests_data/tests_minimization.txt", "a")
        f.write(w)
        f.close()

    def test_minimization_presentation2(self):
        """Test the automaton from the minimization presentation. (guide)"""
        automaton_str = """
        Automaton:
            Symbols: 01

            A
            B final
            C final
            D 
            E 
            F final

            ini A -0-> B
            A -1-> C
            B -0-> D
            B -1-> E
            C -0-> E 
            C -1-> D
            D -0-> F
            D -1-> F
            E -0-> F
            E -1-> F
            F -0-> F
            F -1-> F
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: 01

            A
            BC final
            DE
            F final

            ini A -0-> BC
            A -1-> BC
            BC -0-> DE
            BC -1-> DE
            DE -0-> F
            DE -1-> F
            F -0-> F
            F -1-> F
        """
        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)

        w = '''Test from presentation2:\n\nRecived:\n'''

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(DeterministicFiniteAutomaton.to_minimized(automaton))
        w += '''\n\n'''

        f = open("tests_data/tests_minimization.txt", "a")
        f.write(w)
        f.close()

    def test_minimization_example1(self):
        """Test the automaton from the minimization example."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0 final
            q1
            q2 final
            q3
            q4 final
            q5

            ini q0 -0-> q1
            q0 -1-> q1
            q1 -0-> q2
            q1 -1-> q2
            q2 -0-> q3
            q2 -1-> q3
            q3 -0-> q4
            q3 -1-> q4
            q4 -0-> q5
            q4 -1-> q5
            q5 -0-> q0
            q5 -1-> q0
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: 01

            q0q2q4 final
            q1q3q5

            ini q0q2q4 -0-> q1q3q5
            q0q2q4 -1-> q1q3q5
            q1q3q5 -0-> q0q2q4
            q1q3q5 -1-> q0q2q4
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)

        w = '''Test from example sheet:\n\nRecived:\n'''

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(DeterministicFiniteAutomaton.to_minimized(automaton))
        w += '''\n\n'''

        f = open("tests_data/tests_minimization.txt", "a")
        f.write(w)
        f.close()

    def test_minimization_example2(self):
        """Test the automaton from the minimization example."""
        automaton_str = """
        Automaton:
            Symbols: ab

            q0 
            q1 final
            q2 
            q3 final
            q4 

            ini q0 -a-> q1
            q0 -b-> q3
            q1 -a-> q2
            q1 -b-> q1
            q2 -a-> q1
            q2 -b-> q2
            q3 -a-> q4
            q3 -b-> q3
            q4 -a-> q3
            q4 -b-> q4
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: ab

            q0 
            q1q3 final
            q2q4

            ini q0 -a-> q1q3
            q0 -b-> q1q3
            q1q3 -a-> q2q4
            q1q3 -b-> q1q3
            q2q4 -a-> q1q3
            q2q4 -b-> q2q4
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)

        w = '''Test from example sheet2:\n\nRecived:\n'''

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(DeterministicFiniteAutomaton.to_minimized(automaton))
        w += '''\n\n'''

        f = open("tests_data/tests_minimization.txt", "a")
        f.write(w)
        f.close()

    def test_minimization_example3(self):
        """Test the automaton from the minimization example."""
        automaton_str = """
        Automaton:
            Symbols: abc

            A final
            B final
            C final
            D final
            E 

            ini A -a-> B
            A -c-> B
            A -b-> C
            B -a-> B
            B -c-> B
            B -b-> C
            C -a-> B
            C -c-> B
            C -b-> D
            D -a-> E
            D -b-> E
            D -c-> E
            E -a-> E
            E -b-> E
            E -c-> E
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: abc

            AB final
            C final
            D final
            E 

            ini AB -a-> AB
            AB -c-> AB
            AB -b-> C
            C -a-> AB
            C -c-> AB
            C -b-> D
            D -a-> E
            D -b-> E
            D -c-> E
            E -a-> E
            E -b-> E
            E -c-> E
        """
        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)

        w = '''Test from example sheet3:\n\nRecived:\n'''

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(DeterministicFiniteAutomaton.to_minimized(automaton))
        w += '''\n\n'''

        f = open("tests_data/tests_minimization.txt", "a")
        f.write(w)
        f.close()

if __name__ == '__main__':
    unittest.main()
