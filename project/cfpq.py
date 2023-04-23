from collections import defaultdict
from typing import Set, Tuple

import networkx as nx
import numpy as np
import scipy.sparse as sp
from pyformlang.cfg import CFG, Terminal, Variable

from project.context_free_grammar_util import cfg_to_weak_cnf, get_cfg_from_file
from project.g_util import load_graph


def cfpq_matrix_from_file(graph: str, cfg: str) -> Set:
    graph_as_MultiDiGrpah = load_graph(graph)
    cfg_as_cfg = get_cfg_from_file(cfg)
    return cfpq(graph_as_MultiDiGrpah, cfg_as_cfg, "matrix")


def cfpq_hellings_from_file(graph: str, cfg: str) -> Set:
    graph_as_MultiDiGrpah = load_graph(graph)
    cfg_as_cfg = get_cfg_from_file(cfg)
    return cfpq(graph_as_MultiDiGrpah, cfg_as_cfg, "hellings")


def cfpq(graph: nx.MultiDiGraph, cfg: CFG, algo: str = "hellings",
    start_nodes: Set = None, final_nodes: Set = None, start_symbol: Variable = Variable("S")
) -> Set:
    """
    Executes query on graph with Hellings algorithm
    :param graph: Graph as MultiDiGraph
    :param cfg: CFG
    :param algo: Algorithm to run cfpq
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
    if (algo == "hellings"):
        algo_result = hellings_(cfg, graph)
    elif (algo == "matrix"):
        algo_result = matrix_(cfg, graph)
    else:
        raise Exception("Not supported algorithm")

    for u, var_1, v in algo_result:
        if start_symbol == var_1 and u in start_nodes and v in final_nodes:
            result.add((u, v))
    return result


def hellings_(cfg: CFG, graph: nx.MultiDiGraph) -> Set[Tuple]:
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


def matrix_(cfg: CFG, graph: nx.MultiDiGraph) -> Set[Tuple]:
    """
    Calculate reachability between all pirs of vertices with Matrix algorithm on given CFG and graph
    :param cfg: CFG
    :param graph: Graph
    :return: triplets (vertex, variable, vertex) Vertex - NonTerminal - Vertex
    """
    node_count = graph.number_of_nodes()
    if node_count == 0:
        return set()

    wcnf = cfg_to_weak_cnf(cfg)
    matrices = defaultdict(set)
    for var in wcnf.variables:
        matrices[var] = sp.dok_matrix((node_count, node_count), dtype=np.bool_)

    for productions in wcnf.productions:
        matrix = matrices[productions.head]
        l = len(productions.body)
        if l == 0:
            for i in range(node_count):
                matrix[i, i] = 1
            continue
        elif l == 1:
            term = productions.body[0]
            if isinstance(term, Terminal):
                term = term.value
                for v, u, l in graph.edges(data="label"):
                    if l == term:
                        matrix[v, u] = 1
        elif l == 2:
            continue

    for var, matrix in matrices.items():
        matrix.tocsr()

    while True:
        new_matrices = defaultdict(set)
        for var in wcnf.variables:
            new_matrices[var] = sp.csr_matrix((node_count, node_count), dtype=np.bool_)

        for productions in wcnf.productions:
            l = len(productions.body)
            if l != 2:
                continue
            x = matrices[productions.body[0]] * (matrices[productions.body[1]])
            new_matrices[productions.head] += x

        prev_non_zero = defaultdict(set)
        for var, matrix in matrices.items():
            prev_non_zero[var] = matrix.count_nonzero()
        for nt, m in new_matrices.items():
            matrices[nt] += m
        cur_non_zero = defaultdict(set)
        for var, matrix in matrices.items():
            cur_non_zero[var] = matrix.count_nonzero()
        if prev_non_zero == cur_non_zero:
            break

    result = set()
    for var, matrix in matrices.items():
        matrix = matrix.tocoo()
        for u, v, b in zip(matrix.row, matrix.col, matrix.data):
            if b == True:
                result.add((u, var, v))
    return result

