import filecmp
import unittest

from project.parser import validate_program, SyntaxTreeVisitor


class qLangParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_sanity_check(self):
        assert validate_program("x = 1;")
        assert not validate_program("x = 1")
        assert validate_program("")
        assert validate_program("// Hello world")

    def test_assignment(self):
        assert validate_program(
            """
            a = 1234567890;
            b = 6;
            c = "wasd";
            a = b;
            c = a;
            """
        )
        assert not validate_program(
            """
            a1 = 5;
            """
        )

    def test_lambda(self):
        assert validate_program("a = lam (x) -> {y};")
        assert validate_program("a = map(lam (x) -> {y}, x);")
        assert validate_program("a = filter(lam (x) -> {y}, x);")

    def test_graph_expr(self):
        assert validate_program("a = setStart(u, v);")
        assert validate_program("a = setFinal(u, v);")
        assert validate_program("a = addStart(u, v);")
        assert validate_program("a = addFinal(u, v);")
        assert validate_program("a = getStart(u);")
        assert validate_program("a = getFinal(u);")
        assert validate_program("a = getReachable(u);")
        assert validate_program("a = getVertices(u);")
        assert validate_program("a = getEdges(u);")
        assert validate_program("a = getLabels(u);")

        assert not validate_program("a = setstart(u, v);")
        assert not validate_program("a = setfinal(u, v);")
        assert not validate_program("a = addstart(u, v);")
        assert not validate_program("a = addfinal(u, v);")
        assert not validate_program("a = getstart(u);")
        assert not validate_program("a = getfinal(u);")
        assert not validate_program("a = getreachable(u);")
        assert not validate_program("a = getvertices(u);")
        assert not validate_program("a = getedges(u);")
        assert not validate_program("a = getlabels(u);")


    def test_bool_expr(self):
        assert validate_program("a = x & y;")
        assert validate_program("a = x == y;")
        assert validate_program("a = x != y;")
        assert validate_program("a = x || y;")
        assert validate_program("a = x in y;")

    def test_load(self):
        assert validate_program("g = load(\"path\");")

    def test_tree(self):
        path = "path.dot"
        SyntaxTreeVisitor("x = 1;").save_in_dot(path)
        assert filecmp.cmp(path, "./tests/expected_syntax_graph")


