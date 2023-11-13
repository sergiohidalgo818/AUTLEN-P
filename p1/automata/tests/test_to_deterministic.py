"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(self, automaton, expected):
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_deterministic()
        equiv_map = deterministic_automata_isomorphism(expected, transformed)

        self.assertTrue(equiv_map is not None)

    def test_case1(self):
        """Test Case 1."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        
        ini q0 -0-> qf
        qf -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        empty
        
        ini q0 -0-> qf
        q0 -1-> empty
        qf -0-> empty
        qf -1-> qf
        empty -0-> empty
        empty -1-> empty
        """

        w = '''Test Case 1:\n\nRecived:\n'''

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(automaton.to_deterministic())
        w += '''\n\n'''

        f = open("tests_data/test_to_deterministic.txt", "w")
        f.write(w)
        f.close()

    def test_case2(self):
        """Test Case 2."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        A
        B final
        
        ini A -0-> B
        B -0-> B
        B -1-> B
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        A
        B final
        empty
        
        ini A -0-> B
        A -1-> empty
        B -0-> B
        B -1-> B
        empty -0-> empty
        empty -1-> empty
        """

        w = '''Test Case 2:\n\nRecived:\n'''

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(automaton.to_deterministic())
        w += '''\n\n'''

        f = open("tests_data/test_to_deterministic.txt", "a")
        f.write(w)
        f.close()

    def test_case3(self):
        """Test Case 3. (No empty state)"""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        A
        B final
        
        ini A -0-> A
        A -1-> A
        A -1-> B
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        A
        AB final
        
        ini A -0-> A
        A -1-> AB
        AB -0-> A
        AB -1-> AB
        """

        w = '''Test Case 3:\n\nRecived:\n'''

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(automaton.to_deterministic())
        w += '''\n\n'''

        f = open("tests_data/test_to_deterministic.txt", "a")
        f.write(w)
        f.close()

    def test_case4(self):
        """Test Case 4. (States that share relation)"""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        A
        B
        C final
        
        ini A -0-> A
        A -1-> A
        A -0-> B
        B -1-> C
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        A
        AB
        AC final
        
        ini A -0-> AB
        A -1-> A
        AB -0-> AB
        AB -1-> AC
        AC -0-> AB
        AC -1-> A
        """

        w = '''Test Case 4:\n\nRecived:\n'''

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(automaton.to_deterministic())
        w += '''\n\n'''

        f = open("tests_data/test_to_deterministic.txt", "a")
        f.write(w)
        f.close()


    def test_case5(self):
        """Test Case 5. (State creation and multiple relation)"""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        A
        B
        C final
        
        ini A -0-> A
        A -1-> A
        A -1-> B
        B -0-> C
        B -1-> C
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        A
        AB
        AC final
        ABC final
        
        ini A -0-> A
        A -1-> AB
        AB -0-> AC
        AB -1-> ABC
        AC -0-> A
        AC -1-> AB
        ABC -0-> AC
        ABC -1-> ABC
        """
        w = '''Test Case 5:\n\nRecived:\n'''

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
      
        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(automaton.to_deterministic())
        w += '''\n\n'''
   
        f = open("tests_data/test_to_deterministic.txt", "a")
        f.write(w)
        f.close()
   
    def test_case6(self):
        """Test Case 6. (Similar to test 4, but changing relation)"""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        q1
        q2 final
        
        ini q0 -0-> q0
        q0 -1-> q0
        q0 -1-> q1
        q1 -0-> q2
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        q0q1
        q0q2 final
        
        ini q0 -0-> q0
        q0 -1-> q0q1
        q0q1 -0-> q0q2
        q0q1 -1-> q0q1
        q0q2 -0-> q0
        q0q2 -1-> q0q1
        """


        w = '''Test Case 6:\n\nRecived:\n'''

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

        w += write_dot(automaton)
        w += '''\nProcessed:\n'''
        w += write_dot(automaton.to_deterministic())
        w += '''\n\n'''

        f = open("tests_data/test_to_deterministic.txt", "a")
        f.write(w)
        f.close()

if __name__ == '__main__':
    unittest.main()
