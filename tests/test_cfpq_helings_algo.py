import unittest

from pyformlang.cfg import CFG

from project.cfpq import cfpq
from project.g_util import build_two_cycle_labeled_graph


class CfpqHellingsAlgoTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        cfg = "S -> epsilon"
        graph = build_two_cycle_labeled_graph(1, 1, ("a", "b"))
        expected = {(0, 0), (1, 1), (2, 2)}
        actual = cfpq(graph, CFG.from_text(cfg), "hellings")
        assert actual == expected

    def test_2(self):
        cfg = """
            S -> a S
            S -> epsilon
            """
        graph = build_two_cycle_labeled_graph(1, 1, ("a", "b"))
        expected = {(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)}
        actual = cfpq(graph, CFG.from_text(cfg), "hellings")
        assert actual == expected

    def test_3(self):
        cfg = """
            S -> a b
            S -> a S1
            S1 -> S b
            """
        graph = build_two_cycle_labeled_graph(2, 1, ("a", "b"))
        expected = {(0, 0), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3)}
        actual = cfpq(graph, CFG.from_text(cfg), "hellings", {0, 1, 2, 3}, {0, 1, 2, 3})
        assert actual == expected

    def test_4(self):
        cfg = """
        S -> S b | epsilon
        """
        graph = build_two_cycle_labeled_graph(1, 1, ("a", "b"))
        expected = {(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)}
        actual = cfpq(graph, CFG.from_text(cfg), "hellings")
        assert actual == expected