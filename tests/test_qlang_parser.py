import filecmp
import unittest

from project.parser import validate_program, SyntaxTreeVisitor


class qLangParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_sanity_check(self):
        assert validate_program("bind x = 1;")
        assert not validate_program("x = 1")
        assert validate_program("")
        assert validate_program("// Hello world")

    def test_assignment(self):
        assert validate_program(
            """
            bind a = 1234567890;
            bind b = 6;
            bind c = "wasd";
            bind a = b;
            bind c = a;
            """
        )

    def test_lambda(self):
        assert validate_program("bind a = lam (x) -> {y};")
        assert validate_program("bind a = map(lam (x) -> {y}, x);")
        #assert validate_program("bind a = filter(lam (x) -> {y}, x);")

    def test_graph_expr(self):
        assert validate_program("bind a = setStart(u, v);")
        assert validate_program("bind a = setFinal(u, v);")
        assert validate_program("bind a = addStart(u, v);")
        assert validate_program("bind a = addFinal(u, v);")
        assert validate_program("bind a = getStart(u);")
        assert validate_program("bind a = getFinal(u);")
        assert validate_program("bind a = getReachable(u);")
        assert validate_program("bind a = getVertices(u);")
        assert validate_program("bind a = getEdges(u);")
        assert validate_program("bind a = getLabels(u);")

        assert not validate_program("bind a = setstart(u, v);")
        assert not validate_program("bind a = setfinal(u, v);")
        assert not validate_program("bind a = addstart(u, v);")
        assert not validate_program("bind a = addfinal(u, v);")
        assert not validate_program("bind a = getstart(u);")
        assert not validate_program("bind a = getfinal(u);")
        assert not validate_program("bind a = getreachable(u);")
        assert not validate_program("bind a = getvertices(u);")
        assert not validate_program("bind a = getedges(u);")
        assert not validate_program("bind a = getlabels(u);")


    def test_bool_expr(self):
        assert validate_program("bind a = x && y;")
        assert validate_program("bind a = x == y;")
        assert validate_program("bind a = x != y;")
        assert validate_program("bind a = x || y;")

    def test_load(self):
        assert validate_program("bind g = load(\"path\");")

    def test_tree(self):
        path = "path.dot"
        SyntaxTreeVisitor("bind x = 1;").save_in_dot(path)
        assert filecmp.cmp(path, "./tests/expected_syntax_graph.dot")


