from typing import Set

import networkx as nx
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton


def regex_to_min_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    return Regex(regex_str).to_epsilon_nfa().minimize()


def graph_to_nfa(graph: nx.MultiDiGraph, start_set: Set = None, final_set: Set = None) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()
    all_nodes = set(graph.nodes)
    for node_from, node_to, label in graph.edges(data="label"):
        nfa.add_transition(node_from, label, node_to)

    if start_set is None:
        start_set = all_nodes
    for node in start_set:
        nfa.add_start_state(node)

    if final_set is None:
        final_set = all_nodes
    for node in final_set:
        nfa.add_final_state(node)

    return nfa

