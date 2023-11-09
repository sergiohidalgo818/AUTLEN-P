from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic
from collections import deque
from functools import cmp_to_key
import copy
import queue
import numpy

def comparator(x, y):
        '''
        Compare 2 states 
        '''
        # gets the name in lowkeys
        namex=x.name.lower()
        namey=y.name.lower()

        # empty is the first on the list
        if namex=='empty':
            return -1
        elif namey=='empty':
            return 1
        
        # initial is second
        if namex=='initial':
            return -1
        elif namey=='initial':
            return 1
        
        # qf or final should be the last one
        if namex=='qf' or namex=='final':
            return 1
        elif namey =='qf' or namey=='final':
            return -1
        
        # in any other case substract numbers
        return int(namex[1:]) - int(namey[1:])

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
      
            # sort list with custom cmp
            sortedlist = sorted(state_list, key=cmp_to_key(comparator))

            namestate = ""
            final = False
            for i in sortedlist:
                # the state name will be equivalent to all the name of the states
                namestate += "q"+i.name[1:]+","
                # if it the final state is among the states
                if i.is_final:
                    # it will automatically became a true state
                    final = True
            # slice to eliminate final comma
            namestate = namestate[:-1]

            # return the new state
            return State(namestate, final)

        # To avoid circular imports
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)

        # creates the new initial state
        initial = create_state(evaluator.current_states)
        # and the table of future transitions
        table = dict()

        # queue to check all the new states
        q = queue.Queue()
        q.put(evaluator.current_states)
        # set of new states
        newstates = set()
        newstates.add(initial)

        # empty state
        empty_state = State("empty", False)

        # while is not empty
        while not q.empty():
            # it will extract the next state on queue
            state = q.get()

            # then create a new state from that one
            newstate = create_state(state)

            # loop to check all the transitions of that newstate
            for sym in finiteAutomaton.symbols:
                # current states is now the extracted state
                evaluator.current_states = state
                # evaluate it
                evaluator.process_symbol(sym)

                # if its the first iteration creates a dict
                if newstate not in table.keys():
                    # with newstate as key
                    table[newstate] = dict()

                # if its an empty set
                if len(evaluator.current_states) == 0:
                    # its the empty state
                    process_state = empty_state
                    newstates.add(process_state)
                else:
                    # if not, create a new state
                    process_state = create_state(evaluator.current_states)

                # and add new set of states (with only the new state)
                table[newstate][sym] = set()
                table[newstate][sym].add(process_state)

                # if its not new
                if process_state not in newstates:
                    # add it to the set and the queue
                    newstates.add(process_state)
                    q.put(evaluator.current_states)

        # create a new entry on dict for empty state
        table[empty_state] = dict()
        # all symbols go to that same state
        for sym in finiteAutomaton.symbols:
            table[empty_state][sym] = set()
            table[empty_state][sym].add(empty_state)

        # creates deterministic automaton
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


        # To avoid circular imports
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(dfa)

        q = queue.Queue()
        q.put(evaluator.current_states)


        # set of accesible states
        accesible_states = set()
        accesible_states.add(dfa.initial_state)

        # while is not empty
        while not q.empty():
            # it will extract the next state on queue
            state = q.get()

            # loop to check all the transitions of that state
            for sym in dfa.symbols:

                # current states is now the extracted state
                evaluator.current_states = state

                # evaluate it
                evaluator.process_symbol(sym)
                
                # if there are states on current_states
                if len(evaluator.current_states) > 0:
                    # flag to check if the current states have been added to queue
                    flag_addqueue=False

                    for next_state in evaluator.current_states:
                        # if the next state has not been added
                        if next_state not in accesible_states:
                            
                            if not flag_addqueue:
                                # add current states if flag is false
                                q.put(evaluator.current_states)
                                flag_addqueue=True

                            # add the next state to accesible states
                            accesible_states.add(next_state)

        # sorted list of the states
        accesible_list=sorted(list(accesible_states), key=cmp_to_key(comparator))

        # create an array for the equivalence
        xtable = len(accesible_list)
        class_table = numpy.ndarray(shape=(2, xtable))
        
        # first iteration
        for i in range(xtable):
            class_table[0][i] =int(accesible_list[i].is_final)
            class_table[1][i] = None 
        
        class_table[1][0] =0

        for i in range(1, xtable):
            if class_table[1][i] != None:
                if class_table[1][i] == class_table[1][0]:
                    # en proceso
                    pass

        return dfa