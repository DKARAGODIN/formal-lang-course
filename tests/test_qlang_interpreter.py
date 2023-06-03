import unittest
import io

from project.g_util import load_graph
from project.interpreter import interpret as i, iterate_nfa
from project.parser import parse
from project.regex_util import graph_to_nfa, regex_string_to_min_dfa


def interpret_to_str(*args, **kwargs):
    with io.StringIO() as output:
        kwargs["out"] = output
        i(*args, **kwargs)
        return output.getvalue()


class qLangInterpreter(unittest.TestCase):
    def setUp(self):
        pass

    def test_sanity_check(self):
        assert True

    def test_empty_program(self):
        assert interpret_to_str(parse("")) == ""
        assert interpret_to_str(parse("// Hello world")) == ""

    def test_very_simple_print_program(self):
        actual = interpret_to_str(parse("bind a = \"test\"; print a;"))
        expected = "test\n"
        assert actual == expected

    def test_literals(self):
        actual = i(parse("\"hello\"", "expr"))
        expected = "hello"
        assert actual.value == expected

        actual = i(parse("1", "expr"))
        expected = 1
        assert actual.value == expected

        actual = i(parse("{1}", "expr"))
        expected = {1}
        assert actual.value == expected

        actual = i(parse("{1,2,3}", "expr"))
        expected = {1, 2, 3}
        assert actual.value == expected

        actual = i(parse("{1,2,3, \"Chetire\"}", "expr"))
        expected = {1, 2, 3, "Chetire"}
        assert actual.value == expected

        actual = i(parse("{}", "expr"))
        expected = {}
        assert actual.value == expected

        actual = i(parse("{              }", "expr"))
        expected = {}
        assert actual.value == expected

    def test_interpret(self):
        i(parse("bind x = map (lam (x) -> { x }, a);"))
        i(parse("bind x = filter (lam (x) -> { x }, a);"))

    def test_load(self):
        actual = i(parse("load(\"wc\");", "expr"))
        expected = graph_to_nfa(load_graph("wc"))
        assert actual.value == expected

    def test_get_start(self):
        actual = i(parse("getStart(\"a\");", "expr"))
        expected = {"0"}
        assert actual.value == expected

        actual = i(parse("getStart(\"a*\");", "expr"))
        expected = {"0;1;2;1;2;3"}
        assert actual.value == expected

    def test_get_final(self):
        actual = i(parse("getFinal(\"a\");", "expr"))
        expected = {"1"}
        assert actual.value == expected

        actual = i(parse("getFinal(\"a*\");", "expr"))
        expected = {"0;1;2;1;2;3"}
        assert actual.value == expected

    def test_set_start(self):
        actual = i(parse("setStart(\"a\", {2});", "expr"))
        expected = regex_string_to_min_dfa("a")
        expected.start_states.clear()
        expected.add_start_state(2)
        assert actual.value == expected

    def test_set_final(self):
        actual = i(parse("setFinal(\"a\", {2});", "expr"))
        expected = regex_string_to_min_dfa("a")
        expected.final_states.clear()
        expected.add_final_state(2)
        assert actual.value == expected

    def test_add_start(self):
        actual = i(parse("addStart(\"a\", {2});", "expr"))
        expected = regex_string_to_min_dfa("a")
        expected.add_start_state(2)
        assert actual.value == expected

    def test_add_final(self):
        actual = i(parse("addFinal(\"a\", {2});", "expr"))
        expected = regex_string_to_min_dfa("a")
        expected.add_final_state(2)
        assert actual.value == expected

    def test_get_reachable(self):
        actual = i(parse("getReachable(\"a\");", "expr"))
        expected = regex_string_to_min_dfa("a")
        assert actual.value == expected._get_reachable_states()

    def test_get_vertices(self):
        actual = i(parse("getVertices(\"a\");", "expr"))
        expected = regex_string_to_min_dfa("a")
        assert actual.value == expected.states

    def test_get_edges(self):
        actual = i(parse("getEdges(\"a\");", "expr"))
        expected = regex_string_to_min_dfa("a")
        expected_transitions = {(u, l, v) for u, l, v in iterate_nfa(expected)}
        assert actual.value == expected_transitions

    def test_get_labels(self):
        actual = i(parse("getLabels(\"a\");", "expr"))
        expected = regex_string_to_min_dfa("a")
        expected_labels = expected.symbols
        assert actual.value == expected_labels

    def test_equals(self):
        actual = i(parse("1 == 1", "expr"))
        assert actual.value
        actual = i(parse("\"a\" == \"a\"", "expr"))
        assert actual.value
        actual = i(parse("{0,1} == {1,0}", "expr"))
        assert actual.value

    def test_not_equals(self):
        actual = i(parse("1 != 1", "expr"))
        assert not actual.value
        actual = i(parse("\"a\" != \"a\"", "expr"))
        assert not actual.value
        actual = i(parse("{0,1} != {1,0}", "expr"))
        assert not actual.value

    def test_in(self):
        actual = i(parse("1 in {1,0}", "expr"))
        assert actual.value
        actual = i(parse("0 in {1,0}", "expr"))
        assert actual.value
        actual = i(parse("\"1\" in {1,0}", "expr"))
        assert not actual.value
        actual = i(parse("2 in {1,0}", "expr"))
        assert not actual.value

    def test_concat_and_intersect_NFA(self):
        i(parse('load("wc") && load("wc")', "expr"))
        i(parse('load("wc") || load("wc")', "expr"))

    def test_concat_and_intersect_set(self):
        actual = i(parse('{1} && {2}', "expr"))
        expected = {1,2}
        assert actual.value == expected
        actual = i(parse('{1} || {2}', "expr"))
        expected = set()
        assert actual.value == expected

    def test_concat_and_intersect_string(self):
        actual = i(parse('"1" || "2"', "expr"))
        expected = "12"
        assert actual.value == expected

