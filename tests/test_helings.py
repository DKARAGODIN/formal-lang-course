import unittest

from pyformlang.cfg import CFG
from project.g_util import build_two_cycle_labeled_graph
from project.rpq import context_free_path_query

class HellingsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        cfg = "S -> epsilon"
        graph = build_two_cycle_labeled_graph(1, 1, ("a", "b"))
        expected = {(0, 0), (1, 1), (2, 2)}
        assert context_free_path_query(graph, CFG.from_text(cfg)) == expected

    def test_2(self):
        cfg = """
            S -> a S
            S -> epsilon
            """
        graph = build_two_cycle_labeled_graph(1, 1, ("a", "b"))
        expected = {(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)}
        assert context_free_path_query(graph, CFG.from_text(cfg)) == expected

    def test_3(self):
        cfg = """
            S -> a b
            S -> a S1
            S1 -> S b
            """
        graph = build_two_cycle_labeled_graph(2, 1, ("a", "b"))
        expected = {(0, 0), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3)}
        assert context_free_path_query(graph, CFG.from_text(cfg), {0, 1, 2, 3}, {0, 1, 2, 3}) == expected