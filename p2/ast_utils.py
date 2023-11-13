from ast import NodeVisitor
from ast import iter_fields, AST, If

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
    states : list[tuple]
    # transitions are stored as [transition_label]:(state, state)
    transitions : dict[tuple]

    def __init__(self) -> None:
        self.digraph = '''digraph {\n'''
        self.state_count = 0
        self.states = list()
        self.transitions = dict()
    
    def generic_visit(self, node):
        '''
        Generic visit of the code
        '''
        print(node.__class__.__name__)
        self.states= ("s"+self.state_count, node.__class__.__name__+"()")
        self.digraph += "s"+self.state_count+"[label="+node.__class__.__name__+"()"+", "
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    self.if_visited = False
                    if isinstance(item, AST):
                        self.visit(item)
                    elif isinstance(value, AST):
                        self.visit(value)
        

        return self.digraph + '''}'''
    