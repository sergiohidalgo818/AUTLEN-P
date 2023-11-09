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
    namex = x.name.lower()
    namey = y.name.lower()



    # initial is first of the list
    if namex == 'initial':
        return -1
    elif namey == 'initial':
        return 1
    
    # empty should be the last one
    if namex == 'empty':
        return 1
    elif namey == 'empty':
        return -1

    # preceded from the qf
    if namex == 'qf' or namex == 'final':
        return 1
    elif namey == 'qf' or namey == 'final':
        return -1
    


    if namex[1:].isdigit() and namex[1:].isdigit():

        # in any other case substract numbers
        return int(namex[1:]) - int(namey[1:])

    # in case is A,B,C,D..
    valx = 0
    valy = 0

    for i in namex:
        valx += ord(i)

    for i in namey:
        valy += ord(i)

    return valx - valy


def create_state(state_set: set) -> State:
    '''
    Function that creates a new state from a set of states
    '''
    # it creates a list from the set
    state_list = list(state_set)

    # sort list with custom cmp
    sortedlist = sorted(state_list, key=cmp_to_key(comparator))

    namestate = ""
    final = False

    # if states are named A,B,C they doesnt have a number
    qsnnumbers = False
    if sortedlist[0].name[1:0].isdigit():
        qsnnumbers = True

    for i in sortedlist:
        # the state name will be equivalent to all the name of the states
        if qsnnumbers:
            namestate += "q"+i.name[1:]+","
        else:
            namestate += i.name

        # if it the final state is among the states
        if i.is_final:
            # it will automatically became a true state
            final = True

    # slice to eliminate final comma
    if qsnnumbers:
        namestate = namestate[:-1]

    # return the new state
    return State(namestate, final)


class DeterministicFiniteAutomaton(FiniteAutomaton):

    @staticmethod
    def to_deterministic(finiteAutomaton: FiniteAutomaton):
        """
        Returns an equivalent deterministic finite automaton.
        """

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
        empty_state = State("Empty", False)

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
        evaluatorpre = FiniteAutomatonEvaluator(dfa)

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
                    flag_addqueue = False

                    for next_state in evaluator.current_states:
                        # if the next state has not been added
                        if next_state not in accesible_states:

                            if not flag_addqueue:
                                # add current states if flag is false
                                q.put(evaluator.current_states)
                                flag_addqueue = True

                            # add the next state to accesible states
                            accesible_states.add(next_state)

        # sorted list of the states
        accesible_list = sorted(list(accesible_states),
                                key=cmp_to_key(comparator))

        # create an array for the equivalence
        xtable = len(accesible_list)
        class_table = numpy.ndarray(shape=(2, xtable))

        # first iteration
        for i in range(xtable):
            class_table[0][i] = int(accesible_list[i].is_final)
            class_table[1][i] = None

        while 1:
            # class counter
            classcont = 0
            for j in range(xtable):
                # if its NaN (None, without class)
                if numpy.isnan(class_table[1][j]):
                    # it gets one
                    class_table[1][j] = classcont
                    classcont += 1

                    # this is the loop that compares transitions
                    for i in range(1, xtable):
                        same_class = True

                        # if no class
                        if numpy.isnan(class_table[1][i]):
                            # and the next state on the previous row
                            # equals the previous class from the same state
                            # that we assigned the class on the top loop
                            if class_table[0][i] == class_table[0][j]:

                                # for each symbol
                                for sym in dfa.symbols:
                                    # checks transitions
                                    evaluatorpre.current_states = {
                                        accesible_list[j]}
                                    evaluator.current_states = {
                                        accesible_list[i]}
                                    evaluatorpre.process_symbol(sym)
                                    evaluator.process_symbol(sym)

                                    # gets the state itself
                                    pre_state = evaluatorpre.current_states.pop()
                                    state_now = evaluator.current_states.pop()

                                    # and checks if the classes dont match
                                    if class_table[0][accesible_list.index(pre_state)] != class_table[0][accesible_list.index(state_now)]:
                                        same_class = False
                                        break
                                # if al their transitions classes match, then assigns the value
                                # from the new assigned class on the top loop
                                if same_class:
                                    class_table[1][i] = class_table[1][j]

            # if both rows are equal its finished
            if numpy.array_equal(class_table[0], class_table[1]):
                break
            else:
                # if not the second row becomes the first
                for i in range(xtable):
                    class_table[0][i] = class_table[1][i]
                    class_table[1][i] = None

        # Checks the bigger class
        check_bigger = [class_table[0][i] for i in range(len(class_table[0]))]
        check_bigger.sort(reverse=True)
        new_tam_states = int(check_bigger[0])+1

        # list of sets for the new states
        list_set_states = [set() for i in range(new_tam_states)]
        new_states = set()

        for i in range(xtable):
            list_set_states[int(class_table[0][i])].add(accesible_list[i])

        new_transitions_dict = dict()

        for i in range(new_tam_states):
            # it creates the new states
            aux_state = create_state(list_set_states[i])
            new_states.add(aux_state)

            new_transitions_dict[aux_state] = dict()

            for symb in dfa.symbols:
                # and checks all transitions
                evaluator.current_states = list_set_states[i]
                evaluator.process_symbol(symb)
                new_transitions_dict[aux_state][symb] = set()

                # if its not on the list of set states
                if evaluator.current_states not in list_set_states:
                    aux_current = evaluator.current_states.pop()

                    # gets the index of the class (which is the same index for the set of the new state)
                    evaluator.current_states = list_set_states[int(class_table[0][accesible_list.index(
                        aux_current)])]
                
                # add the new state (creating it)
                new_transitions_dict[aux_state][symb].add(
                    create_state(evaluator.current_states))


        trans = Transitions(new_transitions_dict)

        aut = FiniteAutomaton(initial_state=create_state(list_set_states[0]), states=new_states,
                              symbols=dfa.symbols, transitions=trans)

        return aut
