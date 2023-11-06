from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic
from collections import deque
import copy
import queue


class DeterministicFiniteAutomaton(FiniteAutomaton):

    @staticmethod
    def to_deterministic(finiteAutomaton: FiniteAutomaton):
        """
        Returns an equivalent deterministic finite automaton.
        """
        # function that creates a new state from a set of states
        def create_state(state_set: set) -> State:
            # it creates a list from the set
            state_list = list(state_set)
            # list comprehension to get list of state names
            state_name = [state.name for state in state_list]
            # list comprehension to get list of finals
            state_final = [state.is_final for state in state_list]
            # state name list shorted
            state_name.sort()
            namestate = ""
            final = False
            # acces of the index of the list
            for i in range(len(state_list)):
                # the state name will be equivalent to all the name of the states
                namestate += "q"+state_name[i][1:]+","
                # if it the final state is among the states
                if state_final[i]:
                    # it will automatically became a true state
                    final = True
            # slice to eliminate final comma
            namestate = namestate[:-1]

            # return the new state
            return State(namestate, final)

        # To avoid circular imports
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)

        initial = create_state(evaluator.current_states)
        table = dict()

        q = queue.Queue()
        q.put(evaluator.current_states)
        newstates = set()
        newstates.add(create_state(evaluator.current_states))

        empty_state = State("empty", False)

        while not q.empty():
            state = q.get()

            newstate = create_state(state)
            for sym in finiteAutomaton.symbols:

                evaluator.current_states = state
                evaluator.process_symbol(sym)

                if newstate not in table.keys():
                    table[newstate] = dict()

                if len(evaluator.current_states) == 0:

                    process_state = empty_state
                    newstates.add(process_state)
                else:
                    process_state = create_state(evaluator.current_states)
                table[newstate][sym] = set()
                table[newstate][sym].add(process_state)

                if process_state not in newstates:
                    newstates.add(process_state)
                    q.put(evaluator.current_states)

        table[empty_state] = dict()
        for sym in finiteAutomaton.symbols:
            table[empty_state][sym] = set()
            table[empty_state][sym].add(empty_state)

        trans = Transitions(table)

        aut = FiniteAutomaton(initial, states=newstates,
                              symbols=finiteAutomaton.symbols, transitions=trans)


        return aut

    @staticmethod
    def to_minimized(dfa):
        """
        Return a equivalent minimal automaton.
        Returns:
            Equivalent minimal automaton.
        """
        # ---------------------------------------------------------------------
        # TO DO: Implement this method...

        # ---------------------------------------------------------------------
        raise NotImplementedError("This method must be implemented.")
