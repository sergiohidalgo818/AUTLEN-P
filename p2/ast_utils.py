from ast import NodeVisitor
from ast import iter_fields, AST, If, arguments
from queue import Queue

class ASTNestedIfCounter(NodeVisitor):

    count : int
    nested_if : int

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
        self.count+=1

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

    digraph : str
    state_count : int
    # states are stored as (label, shape)
    states : Queue
    # transitions are stored as [transition_label]:(state, state)
    transitions : list[tuple]

    def __init__(self) -> None:
        self.digraph = '''digraph {\n'''
        self.state_count = 0
        self.states = Queue()
        self.transitions = dict()
    
    def create_diagraph(self)-> str:
        for i in self.states:
            self.digraph += "s"+str(self.state_count)+'[label="'+i+", shape=box]\n"
            self.state_count+=1 

        return self.digraph+ '''}'''
    
    def generic_visit(self, node):
        '''
        Generic visit of the code
        '''
        print("")
        print(node)

        self.states.put("s"+str(self.state_count)+'[label="'+node.__class__.__name__+'(')
        self.state_count+=1 
        transition = ""
        extras = ""
        
        for field, value in iter_fields(node):
            print(field, value)
            if not isinstance(value, list):
                extras+= field+"='"+str(value)+"', "
            
            else:
                for item in value:
                    self.if_visited = False
                    if isinstance(item, AST):
                        self.visit(item)
                    elif isinstance(value, AST):
                        self.visit(value)
        extras = extras[:-2]
        self.digraph+= self.states.get() +extras +')", shape=box]\n'

        return self.digraph+ '''}'''
    