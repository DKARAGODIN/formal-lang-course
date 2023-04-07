from typing import AbstractSet, NamedTuple, Dict, Iterable

from pyformlang.cfg import Variable, CFG
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex


class Box(NamedTuple):
    var: Variable
    dfa: DeterministicFiniteAutomaton


class RecursiveFiniteAutomata(NamedTuple):
    """
    Represents Recursive Finite Automata (Task1)
    """
    start_symbol: Variable
    boxes: Iterable[Box]

class ECFG(NamedTuple):
    """
    Represents ECFG (Task2)
    """
    start_symbol: Variable
    variables: AbstractSet[Variable]
    productions: Dict[Variable, Regex]


def get_ecfg_from_string(text: str, start_symbol: Variable = Variable("S")) -> ECFG:
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


def get_ecfg_from_file(file: str, start_symbol: Variable = Variable("S")) -> ECFG:
    """
    Constructs ECFG from file (Task 3.2)
    :param file: file path as a string
    :param start_symbol: Start symbol of given ECFG
    :return: ECFG
    """
    with open(file) as f:
        return get_ecfg_from_string(f.read(), start_symbol=start_symbol)


def convert_ecfg_to_RecursiveFiniteAutomata(ecfg: ECFG) -> RecursiveFiniteAutomata:
    """
    Converts ECFG to Recursive Finite Automata (Task 4)
    :param ecfg: Given ECFG
    :return: Recursive Finite Automata from ECFG
    """
    return RecursiveFiniteAutomata(
        start_symbol=ecfg.start_symbol,
        boxes={var: regex.to_epsilon_nfa().to_deterministic() for var, regex in ecfg.productions.items()},
    )


def convert_cfg_to_ecfg(cfg: CFG) -> ECFG:
    """
    Converts CFG to ECFG
    :param cfg: CFG
    :return: ECFG
    """
    productions: Dict[Variable, Regex] = dict()
    for prod in cfg.productions:
        lst = productions.setdefault(prod.head.value, [])
        if prod.body:
            lst.append(".".join(str(e.value) for e in prod.body))
        else:
            lst.append("$")

    productions = {
        head: Regex(" | ".join(f"({elem})" for elem in body))
        for head, body in productions.items()
    }
    return ECFG(
        start_symbol=cfg.start_symbol,
        variables=cfg.variables,
        productions=productions
    )


def minimize_RecursiveFiniteAutomata(rfa: RecursiveFiniteAutomata):
    """
    Minimizes Recursive Finite Automata (Task 5)
    :return: Minimized Recursive Finite Automata
    """
    return RecursiveFiniteAutomata(
        start_symbol=rfa.start_symbol,
        boxes={var: dfa.minimize() for var, dfa in rfa.boxes.items()},
    )
