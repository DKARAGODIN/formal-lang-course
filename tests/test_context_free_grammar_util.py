from pyformlang.cfg import Production, Terminal
from project.context_free_grammar_util import *
import os.path
import unittest


def create_temp_file(file_name, text):
    test_dir_path = os.path.dirname(os.path.abspath(__file__))
    cfg_file = os.sep.join([test_dir_path, file_name])
    with open(cfg_file, "wt") as f:
        f.write(text)
    return cfg_file


class CFXUtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_cfg_to_weak_cnf_1(self):
        cfg_text = """
            S -> a b
            S -> a b | a S
            S -> a S | b S
        """
        weak_cnf = cfg_to_weak_cnf(CFG.from_text(cfg_text))
        assert weak_cnf.is_normal_form() and not weak_cnf.generate_epsilon()

    def test_cfg_to_weak_cnf_2(self):
        cfg_text = """
            S -> a S
            S -> epsilon
        """
        weak_cnf = cfg_to_weak_cnf(CFG.from_text(cfg_text))
        expected = {
            Production(Variable("S"), []),
            Production(Variable("a#CNF#"), [Terminal("a")]),
            Production(Variable("S"), [Variable("a#CNF#"), Variable("S")]),
        }
        assert weak_cnf.productions == expected
        assert weak_cnf.start_symbol == Variable("S")
        assert weak_cnf.terminals.__contains__(Terminal("a"))

    def test_get_cfg_from_file(self):
        file = create_temp_file("cfg.txt", "S -> x")
        cfg = get_cfg_from_file(file)
        expected = {Production(Variable("S"), [Terminal("x")])}
        assert cfg.productions == expected
        os.remove(file)

    def test_get_cfg_from_file_empty(self):
        file = create_temp_file("cfg.txt", "")
        cfg = get_cfg_from_file(file)
        assert cfg.is_empty()
        os.remove(file)
