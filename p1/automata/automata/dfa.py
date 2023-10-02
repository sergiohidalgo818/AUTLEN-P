from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic
from collections import deque

class DeterministicFiniteAutomaton(FiniteAutomaton):
        
    @staticmethod
    def to_deterministic(finiteAutomaton):
        """
        Returns an equivalent deterministic finite automaton.
        """
        
        # To avoid circular imports
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)
        
        #---------------------------------------------------------------------
        # TO DO: Implement this method...

        #---------------------------------------------------------------------
        raise NotImplementedError("This method must be implemented.")

    @staticmethod
    def to_minimized(dfa):
        """
        Return a equivalent minimal automaton.
        Returns:
            Equivalent minimal automaton.
        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        
        #---------------------------------------------------------------------
        raise NotImplementedError("This method must be implemented.")
