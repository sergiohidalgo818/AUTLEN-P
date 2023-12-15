'''
    Sergio Hidalgo y Alexis Canales
'''
from ast import NodeVisitor
from ast import iter_fields, AST, If, arguments
from queue import Queue


class ASTNestedIfCounter(NodeVisitor):

    count: int
    nested_if: int

    def __init__(self) -> None:
        self.count = 0
        self.nested_if = 0

    def generic_visit(self, node):
        '''
        Generic visit of the code
        '''
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.visit(item)
                    elif isinstance(value, AST):
                        self.visit(value)

        return self.nested_if

    def visit_If(self, node):
        '''
        If is visited in this function
        '''
        # +1 because its allready on a if
        self.count += 1

        # explores the if
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    # if finds another explores to
                    if isinstance(item, If):
                        self.visit(item)

        # check if the counter is greater than the max nested if count
        if self.count > self.nested_if:
            self.nested_if = self.count

        self.count = 0


class ASTDotVisitor (NodeVisitor):

    digraph: str
    state_count: int
    states: Queue
    extras_dict: dict
    transitions: Queue
    rec_state: int
    l_parent: int
    l_label: str

    def __init__(self) -> None:
        self.digraph = '''digraph {\n'''
        self.state_count = 0
        self.states = Queue()
        self.extras_dict = dict()
        self.transitions = Queue()
        self.rec_state = 0
        self.l_parent = 0
        self.l_label = ""

    def print_digraph(self):
        '''
            Prints the whole diagraph with the atributes of the class
        '''

        # first iteration outside the loop (because it doesnt have transition)
        s_aux = self.states.get()

        # after we get the state we check if its on extra info dict
        # (the key is the number of the state)
        if s_aux.split('[')[0][1:] in self.extras_dict.keys():
            # if its on the dict add the extra info
            self.digraph += s_aux + \
                self.extras_dict[s_aux.split(
                    '[')[0][1:]][:-2] + ')", shape=box]\n'
        else:
            self.digraph += s_aux + ')", shape=box]\n'

        while not self.states.empty():
            # same as before
            s_aux = self.states.get()
            if s_aux.split('[')[0][1:] in self.extras_dict.keys():
                self.digraph += s_aux + \
                    self.extras_dict[s_aux.split(
                        '[')[0][1:]][:-2] + ')", shape=box]\n'
            else:
                self.digraph += s_aux + ')", shape=box]\n'
            # add transitions
            self.digraph += self.transitions.get() + "\n"

        self.digraph += '''}'''

        print(self.digraph)

    def generic_visit(self, node):
        '''
        Generic visit of the code
        '''
        extras = ""

        # add the states in order to queue
        self.states.put("s"+str(self.state_count) +
                        '[label="'+node.__class__.__name__+'(')

        # if its not the first state
        if self.state_count != 0:
            # add transition
            self.transitions.put("s"+str(self.l_parent) + " -> " +
                                 "s"+str(self.state_count)+'[label="'+self.l_label+'"]')

        actual = self.state_count
        self.state_count += 1

        self.rec_state += 1

        for field, value in iter_fields(node):

            if isinstance(value, list):
                for item in value:
                    self.if_visited = False
                    if isinstance(item, AST):
                        self.l_parent = actual
                        self.l_label = field
                        self.visit(item)

            elif isinstance(value, AST):
                self.l_parent = actual
                self.l_label = field
                self.visit(value)

            else:
                if value == None:
                    extras += field+"="+str(value)+", "
                else:
                    extras += field+"='"+str(value)+"', "

                # add to the extra info dict the extra info
                self.extras_dict[str(actual)] = extras

        self.rec_state -= 1
        # if the recursive state is 0, we have returned
        # to the fist call of the function
        if self.rec_state == 0:
            self.print_digraph()
