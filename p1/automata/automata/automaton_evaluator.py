"""Evaluation of automata."""
from automata.automaton import FiniteAutomaton, State, Transitions
from collections import defaultdict, deque

class FiniteAutomatonEvaluator():
    """
    Definition of an automaton evaluator.

    Args:
        automaton: Automaton to evaluate.

    Attributes:
        current_states: Set of current states of the automaton.

    """

    # automaton: FiniteAutomaton
    # current_states: Set[State]

    def __init__(self, automaton):
        self.automaton = automaton
        
        current_states = {self.automaton.initial_state}
        #---------------------------------------------------------------------
        # TO DO: 
        # add usefull code if necessary
        #---------------------------------------------------------------------
        
        self.current_states = self._complete_lambdas(current_states)
        



    def process_symbol(self, symbol):
        """
        Process one symbol.

        Args:
            symbol: Symbol to consume. Type: str

        """
        #---------------------------------------------------------------------
        
        # TO DO: Implement this method...

        raise NotImplementedError("This method must be implemented.")       
        #---------------------------------------------------------------------

        
    def _complete_lambdas(self, set_to_complete):
        """
        Add states reachable with lambda transitions to the set.

        Args:
            set_to_complete: Current set of states to be completed.
        """
        #---------------------------------------------------------------------
        
        # TO DO: Implement this method...

        raise NotImplementedError("This method must be implemented.")       
        #---------------------------------------------------------------------

        
    def process_string(self, string):
        """
        Process a full string of symbols.

        Args:
            string: String to process.

        """
        for symbol in string:
            self.process_symbol(symbol)


    def is_accepting(self):
        """Check if the current state is an accepting one."""
        #---------------------------------------------------------------------
        
        # TO DO: Implement this method...

        raise NotImplementedError("This method must be implemented.")       
        #---------------------------------------------------------------------
        

    def accepts(self, string):
        """
        Return if a string is accepted without changing state.

        Note: This function is NOT thread-safe.

        """
        old_transitions = self.current_states
        
        try:
            self.process_string(string)
            accepted = self.is_accepting()
        finally:
            self.current_states = old_transitions
        
        return accepted

