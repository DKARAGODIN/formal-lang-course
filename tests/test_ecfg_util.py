import unittest
import os

from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex

from project.context_free_grammar_util import convert_cfg_to_ecfg
from project.ecfg_util import RecursiveFiniteAutomata, ECFG
from project.matrix_util import AdjacencyMatrix
from project.regex_util import regex_to_min_dfa
from tests.test_context_free_grammar_util import create_temp_file


def check_minimize(minimized_rfa: RecursiveFiniteAutomata):
    assert all(
        automaton.is_equivalent_to(automaton.minimize()) for automaton in minimized_rfa.boxes.values()
    )


def check_ecfg(expected_productions: dict, actual_ecfg: ECFG):
    """
    Symbols equality does not work for some unknown reason. Compare inner value of Symbol.
    :param expected_productions:
    :param actual_ecfg:
    :return:
    """
    assert all(
        actual_ecfg.productions[key].head._value == value.head._value for key, value in expected_productions.items()
    )
    assert all(
        expected_productions[key].head._value == value.head._value for key, value in actual_ecfg.productions.items()
    )

def check_ecfg_and_rfa(ecfg: ECFG, rfa: RecursiveFiniteAutomata):
    assert all(
        regex_to_min_dfa(ecfg.productions[key]).is_equivalent_to(rfa.boxes[key].minimize()) for key in ecfg.productions
    )


class ECFGUtilTest(unittest.TestCase):
    def setUp(self):
        pass

    #Group1
    def test_convert_ecfg_to_RecursiveFiniteAutomata_1(self):
        s = ""
        ecfg = ECFG.get_ecfg_from_string(text=s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)

    def test_convert_ecfg_to_RecursiveFiniteAutomata_2(self):
        s = "S -> x"
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)

    def test_convert_ecfg_to_RecursiveFiniteAutomata_3(self):
        s = "S -> a | b* S"
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)

    def test_convert_ecfg_to_RecursiveFiniteAutomata_4(self):
        s = "S -> epsilon"
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)

    def test_convert_ecfg_to_RecursiveFiniteAutomata_5(self):
        s = "S -> epsilon | a S b S"
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)

    # Group2
    def test_convert_cfg_to_ecfg_1(self):
        cfg_as_string = ""
        expected_productions = {}
        actual_ecfg = convert_cfg_to_ecfg(CFG.from_text(cfg_as_string))
        check_ecfg(expected_productions, actual_ecfg)

    def test_convert_cfg_to_ecfg_2(self):
        cfg_as_string = "S -> x"
        expected_productions = {Variable("S"): Regex("x")}
        actual_ecfg = convert_cfg_to_ecfg(CFG.from_text(cfg_as_string))
        check_ecfg(expected_productions, actual_ecfg)

    def test_convert_cfg_to_ecfg_3(self):
        cfg_as_string = "S -> a | b* S"
        expected_productions = {Variable("S"): Regex("(a|((b)*.S))")}
        actual_ecfg = convert_cfg_to_ecfg(CFG.from_text(cfg_as_string))
        check_ecfg(expected_productions, actual_ecfg)

    def test_convert_cfg_to_ecfg_4(self):
        cfg_as_string = "S -> epsilon"
        expected_productions = {Variable("S"): Regex("$")}
        actual_ecfg = convert_cfg_to_ecfg(CFG.from_text(cfg_as_string))
        check_ecfg(expected_productions, actual_ecfg)

    def test_convert_cfg_to_ecfg_5(self):
        cfg_as_string = "S -> epsilon | a S b S"
        expected_productions = {Variable("S"): Regex("$ | a S b S")}
        actual_ecfg = convert_cfg_to_ecfg(CFG.from_text(cfg_as_string))
        check_ecfg(expected_productions, actual_ecfg)

    # Group3
    def test_minimize_RecursiveFiniteAutomata_1(self):
        s = ""
        rfa = ECFG.get_ecfg_from_string(s).convert_to_RecursiveFiniteAutomata()
        minimized_rfa = rfa.minimize_RecursiveFiniteAutomata()
        check_minimize(minimized_rfa)

    def test_minimize_RecursiveFiniteAutomata_2(self):
        s = "S -> x"
        rfa = ECFG.get_ecfg_from_string(s).convert_to_RecursiveFiniteAutomata()
        minimized_rfa = rfa.minimize_RecursiveFiniteAutomata()
        check_minimize(minimized_rfa)

    def test_minimize_RecursiveFiniteAutomata_3(self):
        s = "S -> a | b* S"
        rfa = ECFG.get_ecfg_from_string(s).convert_to_RecursiveFiniteAutomata()
        minimized_rfa = rfa.minimize_RecursiveFiniteAutomata()
        check_minimize(minimized_rfa)

    def test_minimize_RecursiveFiniteAutomata_4(self):
        s = "S -> epsilon"
        rfa = ECFG.get_ecfg_from_string(s).convert_to_RecursiveFiniteAutomata()
        minimized_rfa = rfa.minimize_RecursiveFiniteAutomata()
        check_minimize(minimized_rfa)

    def test_minimize_RecursiveFiniteAutomata_5(self):
        s = "S -> epsilon | a S b S"
        rfa = ECFG.get_ecfg_from_string(s).convert_to_RecursiveFiniteAutomata()
        minimized_rfa = rfa.minimize_RecursiveFiniteAutomata()
        check_minimize(minimized_rfa)

    # Group4
    def test_get_ecfg_from_file_1(self):
        file = create_temp_file("ecfg.txt", "")
        ecfg = ECFG.get_ecfg_from_file(file)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)
        os.remove(file)

    def test_get_ecfg_from_file_2(self):
        file = create_temp_file("ecfg.txt", "S -> x")
        ecfg = ECFG.get_ecfg_from_file(file)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)
        os.remove(file)

    def test_get_ecfg_from_file_3(self):
        file = create_temp_file("ecfg.txt", "S -> a | b* S")
        ecfg = ECFG.get_ecfg_from_file(file)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)
        os.remove(file)

    def test_get_ecfg_from_file_4(self):
        file = create_temp_file("ecfg.txt", "S -> epsilon")
        ecfg = ECFG.get_ecfg_from_file(file)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)
        os.remove(file)

    def test_get_ecfg_from_file_5(self):
        file = create_temp_file("ecfg.txt", "S -> epsilon | a S b S")
        ecfg = ECFG.get_ecfg_from_file(file)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        check_ecfg_and_rfa(ecfg, rfa)
        os.remove(file)

    # Group5
    def test_am_1(self):
        s = ""
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        ams = rfa.get_adjacency_matrices()
        assert ams == {}

    def test_am_2(self):
        s = "S -> x"
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        ams = rfa.get_adjacency_matrices()
        assert len(ams) == 1
        am: AdjacencyMatrix = ams[Variable("S")]
        assert am.get_states_len() == 2
        assert am.get_start_states_len() == 1
        assert am.get_final_states_len() == 1

    def test_am_3(self):
        s = "S -> a | b* S"
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        ams = rfa.get_adjacency_matrices()
        assert len(ams) == 1
        am: AdjacencyMatrix = ams[Variable("S")]
        assert am.get_states_len() == 4
        assert am.get_start_states_len() == 1
        assert am.get_final_states_len() == 2

    def test_am_4(self):
        s = "S -> epsilon"
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        ams = rfa.get_adjacency_matrices()
        assert len(ams) == 1
        am: AdjacencyMatrix = ams[Variable("S")]
        assert am.get_states_len() == 1
        assert am.get_start_states_len() == 1
        assert am.get_final_states_len() == 1

    def test_am_5(self):
        s = "S -> epsilon | a S b S"
        ecfg = ECFG.get_ecfg_from_string(s)
        rfa = ecfg.convert_to_RecursiveFiniteAutomata()
        ams = rfa.get_adjacency_matrices()
        assert len(ams) == 1
        am: AdjacencyMatrix = ams[Variable("S")]
        assert am.get_states_len() == 5
        assert am.get_start_states_len() == 1
        assert am.get_final_states_len() == 2