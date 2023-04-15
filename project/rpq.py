from collections import defaultdict
from typing import Set, Dict, Iterable, Tuple

from pyformlang.cfg import Terminal, CFG, Variable
from scipy import sparse
import networkx as nx

import project.regex_util as regex_util
from project.context_free_grammar_util import cfg_to_weak_cnf
from project.matrix_util import AdjacencyMatrix, intersect_adjacency_matrices, _get_front, _get_reachable_states


def rpq_to_graph_tc(graph: nx.MultiDiGraph, query: str, start_nodes: set = None, final_nodes: set = None) -> set:
    """
    Calculates Regular Path Querying (RPQ) for graph and regular expression with transitive closure method
    :param graph: Graph to send query to
    :param query: Regular Expression to query
    :param start_nodes: Set of start nodes
    :param final_nodes: Set of final nodes
    :return: Regular Path Query as set
    """
    nfa = regex_util.graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_util.regex_string_to_min_dfa(query)
    graph_matrix = AdjacencyMatrix(nfa)
    query_matrix = AdjacencyMatrix(dfa)
    intersected_matrix = intersect_adjacency_matrices(graph_matrix, query_matrix)
    transitive_closure = intersected_matrix.get_transitive_closure()
    start_states = intersected_matrix.start_states
    final_states = intersected_matrix.final_states

    result = set()
    for state_from, state_to in zip(*transitive_closure.nonzero()):
        if state_from in start_states and state_to in final_states:
            result.add((state_from // query_matrix.get_states_len(), state_to // query_matrix.get_states_len()))
    return result


def rpq_to_graph_bfs(
        graph: nx.MultiDiGraph, query: str, start_nodes: Iterable[int] = None, final_nodes: Iterable[int] = None
) -> Set[int]:
    """
    Calculates Regular Path Querying (RPQ) for graph and regular expression with BFS method
    :param graph: Graph to send query to
    :param query: Regular Expression to query
    :param start_nodes: Set of start nodes
    :param final_nodes: Set of final nodes
    :return: Regular Path Querying in Set format
    """

    nfa = regex_util.graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_util.regex_string_to_min_dfa(query)
    graph_matrix = AdjacencyMatrix(nfa)
    query_matrix = AdjacencyMatrix(dfa)
    symbols = graph_matrix.matrix.keys().__and__(query_matrix.matrix.keys())
    front = (
        sparse.vstack(
            [_get_front(graph_matrix, query_matrix, {i}) for i in map(lambda state: graph_matrix.index_by_state(state), graph_matrix.start_states)]
        )
    )
    visited_matrix = front

    while True:
        new_front = sparse.csr_matrix(front.shape, dtype=bool)
        for label in symbols:
            next_front_part = front.__matmul__(graph_matrix.matrix[label])
            for (i, j) in zip(*query_matrix.matrix[label].nonzero()):
                new_front[ j, :] += next_front_part[ i, :]

        front = new_front > visited_matrix
        visited_matrix += front

        if front.count_nonzero() == 0:
            break

    result = _get_reachable_states(graph_matrix, query_matrix, 0, visited_matrix)
    return {end.value for end in result}


def rpq_to_graph_bfs_all_reachable(
        graph: nx.MultiDiGraph, query: str, start_nodes: Iterable[int] = None, final_nodes: Iterable[int] = None
) -> Dict[int, Set[int]]:
    """
    Calculates Regular Path Querying (RPQ) for graph and regular expression with BFS method
    :param graph: Graph to send query to
    :param query: Regular Expression to query
    :param start_nodes: Set of start nodes
    :param final_nodes: Set of final nodes
    :return: Regular Path Querying in Dictionary format
    """

    nfa = regex_util.graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_util.regex_string_to_min_dfa(query)
    graph_matrix = AdjacencyMatrix(nfa)
    query_matrix = AdjacencyMatrix(dfa)
    symbols = graph_matrix.matrix.keys().__and__(query_matrix.matrix.keys())
    front = (
        sparse.vstack(
            [_get_front(graph_matrix, query_matrix, {i}) for i in map(lambda state: graph_matrix.index_by_state(state), graph_matrix.start_states)]
        )
    )
    visited_matrix = front

    while True:
        new_front = sparse.csr_matrix(front.shape, dtype=bool)
        for label in symbols:
            new_front_cut = front.__matmul__(graph_matrix.matrix[label])
            for index in range(len(graph_matrix.start_states)):
                for (i, j) in zip(*query_matrix.matrix[label].nonzero()):
                    new_front[index * query_matrix.get_states_len() + j, :] += \
                        new_front_cut[index * query_matrix.get_states_len() + i, :]

        front = new_front > visited_matrix
        visited_matrix += front

        if front.count_nonzero() == 0:
            break

    result = {
        graph_matrix.state_by_index(start_state_idx):
            _get_reachable_states(graph_matrix, query_matrix, sub_front_idx, visited_matrix)
            for sub_front_idx, start_state_idx in enumerate(
                map(lambda state: graph_matrix.index_by_state(state), graph_matrix.start_states)
            )
        }

    return {start.value: {end.value for end in ends} for (start, ends) in result.items()}


def context_free_path_query(graph: nx.MultiDiGraph, cfg: CFG,
    start_nodes: Set = None, final_nodes: Set = None, start_symbol: Variable = Variable("S")
) -> Set:
    """
    Executes query on graph with Hellings algorithm
    :param graph: Graph as MultiDiGraph
    :param cfg: CFG
    :param start_nodes: Set of start nodes
    :param final_nodes: Set of final nodes
    :param start_symbol: Start symbol, defaults to "S"
    :return: Pairs of vertices that have path between them with given constraints from graph
    """
    cfg._start_symbol = start_symbol

    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes

    result = set()

    for u, var_1, v in hellings(cfg, graph):
        if start_symbol == var_1 and u in start_nodes and v in final_nodes:
            result.add((u, v))
    return result


def hellings(cfg: CFG, graph: nx.MultiDiGraph) -> Set[Tuple]:
    """
    Calculate reachability between all pirs of vertices with Hellings algorithm on given CFG and graph
    :param cfg: CFG
    :param graph: Graph
    :return: triplets (vertex, variable, vertex) Vertex - NonTerminal - Vertex
    """
    node_count = graph.number_of_nodes()
    if node_count == 0:
        return set()

    wcnf = cfg_to_weak_cnf(cfg)
    var_to_var_dict = defaultdict(set)
    result = set()
    queue = []

    for productions in wcnf.productions:
        terminal_to_variable = defaultdict(set)
        eps = set()
        l = len(productions.body)
        if l == 0:
            eps.add(productions.head)
        elif l == 1:
            terminal_to_variable[productions.head].add(productions.body[0])
        elif l == 2:
            var_to_var_dict[productions.head].add((productions.body[0], productions.body[1]))
        for node in graph.nodes:
            for var in eps:
                triplet = (node, var, node)
                result.add(triplet)
                queue.append(triplet)
        for i, j, label in graph.edges(data="label"):
            for n, terms in terminal_to_variable.items():
                if Terminal(label) in terms:
                    triplet = (i, n, j)
                    result.add(triplet)
                    queue.append(triplet)

    while len(queue) != 0:
        u_1, var_1, v_1 = queue.pop(0)
        diff = set()

        for u_2, var_2, v_2 in result:
            if v_2 == u_1:
                for node_count, var_to_var in var_to_var_dict.items():
                    triplet = (u_2, node_count, v_1)
                    if (var_2, var_1) in var_to_var and triplet not in result:
                        diff.add(triplet)
                        queue.append(triplet)

            if v_1 == u_2:
                for node_count, var_to_var in var_to_var_dict.items():
                    triplet = (u_1, node_count, v_2)
                    if (var_1, var_2) in var_to_var and triplet not in result:
                        diff.add(triplet)
                        queue.append(triplet)

        result = result.union(diff)

    return result
