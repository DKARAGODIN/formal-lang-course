from typing import AbstractSet, NamedTuple, Dict, Iterable

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex

from project.matrix_util import AdjacencyMatrix


class RecursiveFiniteAutomata(NamedTuple):
    """
    Represents Recursive Finite Automata (Task1)
    """
    start_symbol: Variable
    boxes: Dict[Variable, DeterministicFiniteAutomaton]

    def minimize_RecursiveFiniteAutomata(self):
        """
        Minimizes Recursive Finite Automata (Task 5)
        :return: Minimized Recursive Finite Automata
        """
        return RecursiveFiniteAutomata(
            start_symbol=self.start_symbol,
            boxes={var: dfa.minimize() for var, dfa in self.boxes.items()},
        )

    def get_adjacency_matrices(self) -> Dict[Variable, AdjacencyMatrix]:
        """
        Returns AdjacencyMatrices
        :return:
        """
        return {var: AdjacencyMatrix(dfa) for var, dfa in self.boxes.items()}

class ECFG(NamedTuple):
    """
    Represents ECFG (Task2)
    """
    start_symbol: Variable
    variables: AbstractSet[Variable]
    productions: Dict[Variable, Regex]

    @staticmethod
    def get_ecfg_from_string(text: str, start_symbol: Variable = Variable("S")):
        """
        Constructs ECFG from string (Task3.1)
        :param text: String representation of ECFG
        :param start_symbol: Start symbol of given ECFG
        :return: ECFG
        """
        variables = set()
        productions = dict()

        for line in text.splitlines():
            if not line.strip():
                continue
            content = [str.strip(elem) for elem in line.split("->")]
            head, body = content
            head = Variable(head)
            body = Regex(body)
            variables.add(head)
            productions[head] = body

        return ECFG(start_symbol=start_symbol, variables=variables, productions=productions)

    @staticmethod
    def get_ecfg_from_file(file: str, start_symbol: Variable = Variable("S")):
        """
        Constructs ECFG from file (Task 3.2)
        :param file: file path as a string
        :param start_symbol: Start symbol of given ECFG
        :return: ECFG
        """
        with open(file) as f:
            return ECFG.get_ecfg_from_string(f.read(), start_symbol=start_symbol)

    def convert_to_RecursiveFiniteAutomata(self) -> RecursiveFiniteAutomata:
        """
        Converts ECFG to Recursive Finite Automata (Task 4)
        :param ecfg: Given ECFG
        :return: Recursive Finite Automata from ECFG
        """
        return RecursiveFiniteAutomata(
            start_symbol=self.start_symbol,
            boxes={var: regex.to_epsilon_nfa().to_deterministic() for var, regex in self.productions.items()},
        )
