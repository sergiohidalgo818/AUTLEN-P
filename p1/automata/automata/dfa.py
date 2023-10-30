from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic
from collections import deque
import copy
import queue
class DeterministicFiniteAutomaton(FiniteAutomaton):
        
    @staticmethod
    def to_deterministic(finiteAutomaton:FiniteAutomaton):
        """
        Returns an equivalent deterministic finite automaton.
        """
        
        # To avoid circular imports
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)
        
        initial = evaluator.current_states
        table = dict()


        q = queue.Queue()
        q.put(evaluator.current_states)
        newstates=set()
        newstates.add(evaluator.current_states)

        while not q.empty():
            state = q.get()
            evaluator.current_states = state
            for sym in finiteAutomaton.symbols:
                evaluator.process_symbol(sym)

                if state not in table.keys():
                    table[state] = dict()
                
                table[state][sym] = evaluator.current_states
                
                if evaluator.current_states not in newstates:
                    newstates.add(evaluator.current_states)
                    q.put(evaluator.current_states)


        
        
        trans = Transitions(table)
        
        aut = FiniteAutomaton(initial, newstates, finiteAutomaton.symbols, trans)

        return aut

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
