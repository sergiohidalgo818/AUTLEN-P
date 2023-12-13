from __future__ import annotations

from collections import deque
from typing import AbstractSet, Collection, MutableSet, Optional, Dict, List, Optional, Set
from copy import deepcopy

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Grammar:
    """
    Class that represents a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Dictionary with the production rules for each non terminal
          symbol of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Dict[str, List[str]],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        if non_terminals != set(productions.keys()):
            raise ValueError(
                f"Set of non-terminals and productions keys should be equal."
            )
        
        for nt, rhs in productions.items():
            if not rhs:
                raise ValueError(
                    f"No production rules for non terminal symbol {nt} "
                )
            for r in rhs:
                for s in r:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )
        
    def firsts(self) -> Dict[str, Set[str]]:
        """
        Method to compute the firsts of each non-terminal.

        Args:
            None

        Returns:
            A dictionary with the Firsts for each non-terminal.
        """
        
        #Initialize previous and current dictionary with different values so it enters the while loop
        previous_dict: Dict[str, Set[str]] = {nt: set("1") for nt in self.non_terminals}
        current_dict: Dict[str, Set[str]] = {nt: set() for nt in self.non_terminals}
        
        #We iterate until nothing changes in the dictionaries between iterations
        while previous_dict != current_dict:
            #Copy current dictionary to the previous one with each iteration
            previous_dict = deepcopy(current_dict)

            for nt in self.non_terminals:

                for string in self.productions.get(nt):
                    
                    #For each production we check if lambda is the result and add it to the corresponding non-terminal first set
                    if string == "":
                        current_dict.get(nt).add(string)
                    #If it isn't lambda then we look at the resulting string
                    else:
                        brk = 0

                        for ch in string:
                            #If the next character is terminal then we add it to the corresponding non-terminal set and end the iteration
                            if ch in self.terminals:
                                current_dict.get(nt).add(str(string[0]))
                                brk = 1
                                break

                            firsts = deepcopy(previous_dict.get(str(ch)))
                            #If the next character is non-terminal and has no lambda in its first set then we add its set to the corresponding non-terminal set and end the iteration
                            if "" not in firsts:
                                current_dict.get(nt).update(firsts)
                                brk = 1
                                break
                            #Otherwise we add the non-terminal first set to the corresponding one and keep iterating
                            firsts.remove("")
                            current_dict.get(nt).update(firsts)
                            
                        #After the loop we check if the whole string was processed and add lambda to the corresponding first set if yes
                        if brk == 0:
                            current_dict.get(nt).add("")
                            
        return previous_dict


    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """
        
        #If the recieved string is empty then its first set will only contain lambda
        if sentence == "":
            firsts = set()
            firsts.add("")
            return firsts
        
        #If the recieved string has any character not included in the accepting language then raises a ValueError Exception
        for ch in sentence:
            if ch not in self.terminals and ch not in self.non_terminals:
                raise ValueError(
                    "La cadena contiene algún caracter no incluído en los terminales ni no terminales"
                )
            
        """previous_dict: Dict[str, Set[str]] = {nt: set("1") for nt in self.non_terminals}
        current_dict: Dict[str, Set[str]] = {nt: set() for nt in self.non_terminals}

        while previous_dict != current_dict:
            previous_dict = deepcopy(current_dict)

            for nt in self.non_terminals:

                for string in self.productions.get(nt):

                    if string == "":
                        current_dict.get(nt).add(string)
                    else:
                        brk = 0

                        for ch in string:
                            if ch in self.terminals:
                                current_dict.get(nt).add(str(string[0]))
                                brk = 1
                                break

                            firsts = previous_dict.get(str(ch))
                            if "" not in firsts:
                                current_dict.get(nt).update(firsts)
                                brk = 1
                                break
                            firsts.remove("")
                            current_dict.get(nt).update(firsts)

                        if brk == 0:
                            current_dict.get(nt).add("")"""
        
        #Initialize the set and get the first set for each non-terminal
        first_set = set()
        brk = 0
        firsts = self.firsts()
        
        #Process the recieved string
        for ch in sentence:
            #If a character is a terminal we add it to the set and discard the rest of the string
            if ch in self.terminals:
                first_set.add(ch)
                brk = 1
                break
            
            #If a character is a non-terminal with no lambda in its first set then we add its first set to the set and discard the rest of the string
            #firsts = previous_dict.get(str(ch))
            if "" not in firsts.get(str(ch)):
                first_set.update(firsts.get(str(ch)))
                brk = 1
                break
            
            #Otherwise we add the non-terminal first set to the set and keep iterating 
            first_set.update(firsts.get(str(ch)))
            
        #If we didn't complete the iteration of the string then we remove lambda from the set
        if brk == 1:
            if "" in first_set:
                first_set.remove("")

        return first_set
        

	# TO-DO: Complete this method for exercise 3... (check)


    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """

        #If the recieved string is empty then return an empty set
        if symbol == "":
            return set()
        
        #If the recieved string is a character not included in the accepting language then raises a ValueError Exception
        if symbol not in self.terminals and symbol not in self.non_terminals:
            raise ValueError(
                "La cadena contiene algún caracter no incluído en los terminales ni no terminales"
            )
        
        #We get a dictionary with the Firsts for each non-terminal
        firsts = self.firsts()
        
        #Initialize previous and current dictionary with different values so it enters the while loop
        previous_dict: Dict[str, Set[str]] = {nt: set("1") for nt in self.non_terminals}
        current_dict: Dict[str, Set[str]] = {nt: set() for nt in self.non_terminals}

        #We iterate until nothing changes in the dictionaries between iterations
        while previous_dict != current_dict:
            #Copy current dictionary to the previous one with each iteration
            previous_dict = deepcopy(current_dict)

            for nt in self.non_terminals:
                #If a non-terminal is the axiom then we add "$" to its follow set
                if nt is self.axiom:
                    current_dict.get(nt).add("$")

                for string in self.productions.get(nt):
                    #For each production we check if lambda is the result and continue if so
                    if string == "":
                        continue
                    else:
                        aux = ""
                        #Otherwise we iterate the resulting string backwards while keeping in aux the last character processed
                        for ch in reversed(string):
                            #If the character being processed is non-terminal and it's the last one in the string then we add to its follow set the set from the non-terminal being processed 
                            if ch in self.non_terminals and aux == "":
                                current_dict.get(ch).update(previous_dict.get(nt))
                                aux = ch
                            
                            #If it's non-terminal and it's followed by a non-terminal then we add the second one's set to the first one's
                            elif ch in self.non_terminals and aux in self.non_terminals:
                                aux_firsts = deepcopy(firsts.get(aux))
                                if "" in aux_firsts:
                                    aux_firsts.remove("")
                                    current_dict.get(ch).update(previous_dict.get(aux))
                                current_dict.get(ch).update(aux_firsts)
                                aux = ch
                            
                            #If it's noon-terminal and is followed by a terminal then we add this terminal to its follow set
                            elif ch in self.non_terminals:
                                current_dict.get(ch).add(aux)
                                aux = ch
                            
                            #If it's terminal we just keep it and continue iterating
                            else:
                                aux = ch

        return previous_dict.get(symbol)

	# TO-DO: Complete this method for exercise 4... (check)


    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """

	# TO-DO: Complete this method for exercise 5...


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None


class LL1Table:
    """
    LL1 table. Initially all cells are set to None (empty). Table cells
    must be filled by calling the method add_cell.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        self.terminals: AbstractSet[str] = terminals
        self.non_terminals: AbstractSet[str] = non_terminals
        self.cells: Dict[str, Dict[str, Optional[str]]] = {nt: {t: None for t in terminals} for nt in non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, non_terminal: str, terminal: str, cell_body: str) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            non_terminal: Non termial symbol (row)
            terminal: Terminal symbol (column)
            cell_body: content of the cell 

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(
                "Trying to add cell for non terminal symbol not included "
                "in table.",
            )
        if terminal not in self.terminals:
            raise ValueError(
                "Trying to add cell for terminal symbol not included "
                "in table.",
            )
        if not all(x in self.terminals | self.non_terminals for x in cell_body):
            raise ValueError(
                "Trying to add cell whose body contains elements that are "
                "not either terminals nor non terminals.",
            )            
        if self.cells[non_terminal][terminal] is not None:
            raise RepeatedCellError(
                f"Repeated cell ({non_terminal}, {terminal}).")
        else:
            self.cells[non_terminal][terminal] = cell_body

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """

        if input_string[-1] != '$':
            raise SyntaxError(
                "La cadena no acaba con el símbolo '$' indicando el final"
            )

        stack = deque()

        stack.append('$')
        stack.append(start)

        i = 0
        nxt = input_string[i]
        if nxt not in self.terminals:
            raise SyntaxError(
                "La cadena contiene algún caracter no incluído en los terminales"
            )

        x = stack.pop()

        while x != '$':
            if x in self.non_terminals:
                prod = self.cells[x][nxt]
                if prod is not None:
                    for char in reversed(prod):
                        stack.append(char)
                else:
                    raise SyntaxError(
                        "No existe ninguna producción para el no terminal " + str(x) + " y el terminal " + str(nxt)
                    )
            elif x in self.terminals:
                if x == nxt:
                    i += 1
                    nxt = input_string[i]
                    if nxt not in self.terminals:
                        raise SyntaxError(
                            "La cadena contiene algún caracter no incluído en los terminales"
                        )
                else:
                    raise SyntaxError(
                        "El terminal en pila y el terminal en la cadena no coinciden"
                    )
            x = stack.pop()

        if x != nxt:
            raise SyntaxError(
                "La pila está vacía pero la cadena no ha terminado"
            )
        elif i == len(input_string):
            raise SyntaxError(
                "La cadena no acaba tras el símbolo '$' que debería indicar el final"
            )
        
        return ParseTree(start)


	# TO-DO: Complete this method for exercise 2... (Check)
    
    
class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection[ParseTree] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children
