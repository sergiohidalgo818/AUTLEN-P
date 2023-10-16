d_t = { "t1" : 0, "t2":1}

if "t1" in d_t:
    print("L0L")

if "t1" in d_t.keys():
    print("LOL2")

from automata.automaton import FiniteAutomaton, State, Transitions

q0 = State("q0", True)
states = set()
states.add(q0)
trans = Transitions({element: dict() for element in states})


