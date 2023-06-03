# Generated from project/qlang.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .qlangParser import qlangParser
else:
    from qlangParser import qlangParser

# This class defines a complete listener for a parse tree produced by qlangParser.
class qlangListener(ParseTreeListener):

    # Enter a parse tree produced by qlangParser#program.
    def enterProgram(self, ctx:qlangParser.ProgramContext):
        pass

    # Exit a parse tree produced by qlangParser#program.
    def exitProgram(self, ctx:qlangParser.ProgramContext):
        pass


    # Enter a parse tree produced by qlangParser#stmt.
    def enterStmt(self, ctx:qlangParser.StmtContext):
        pass

    # Exit a parse tree produced by qlangParser#stmt.
    def exitStmt(self, ctx:qlangParser.StmtContext):
        pass


    # Enter a parse tree produced by qlangParser#print.
    def enterPrint(self, ctx:qlangParser.PrintContext):
        pass

    # Exit a parse tree produced by qlangParser#print.
    def exitPrint(self, ctx:qlangParser.PrintContext):
        pass


    # Enter a parse tree produced by qlangParser#bind.
    def enterBind(self, ctx:qlangParser.BindContext):
        pass

    # Exit a parse tree produced by qlangParser#bind.
    def exitBind(self, ctx:qlangParser.BindContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_set_final.
    def enterExpr_set_final(self, ctx:qlangParser.Expr_set_finalContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_set_final.
    def exitExpr_set_final(self, ctx:qlangParser.Expr_set_finalContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_intersect.
    def enterExpr_intersect(self, ctx:qlangParser.Expr_intersectContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_intersect.
    def exitExpr_intersect(self, ctx:qlangParser.Expr_intersectContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_val.
    def enterExpr_val(self, ctx:qlangParser.Expr_valContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_val.
    def exitExpr_val(self, ctx:qlangParser.Expr_valContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_not_equal.
    def enterExpr_not_equal(self, ctx:qlangParser.Expr_not_equalContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_not_equal.
    def exitExpr_not_equal(self, ctx:qlangParser.Expr_not_equalContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_expr.
    def enterExpr_expr(self, ctx:qlangParser.Expr_exprContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_expr.
    def exitExpr_expr(self, ctx:qlangParser.Expr_exprContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_map.
    def enterExpr_map(self, ctx:qlangParser.Expr_mapContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_map.
    def exitExpr_map(self, ctx:qlangParser.Expr_mapContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_var.
    def enterExpr_var(self, ctx:qlangParser.Expr_varContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_var.
    def exitExpr_var(self, ctx:qlangParser.Expr_varContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_add_start.
    def enterExpr_add_start(self, ctx:qlangParser.Expr_add_startContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_add_start.
    def exitExpr_add_start(self, ctx:qlangParser.Expr_add_startContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_load.
    def enterExpr_load(self, ctx:qlangParser.Expr_loadContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_load.
    def exitExpr_load(self, ctx:qlangParser.Expr_loadContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_get_reachable.
    def enterExpr_get_reachable(self, ctx:qlangParser.Expr_get_reachableContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_get_reachable.
    def exitExpr_get_reachable(self, ctx:qlangParser.Expr_get_reachableContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_get_vertices.
    def enterExpr_get_vertices(self, ctx:qlangParser.Expr_get_verticesContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_get_vertices.
    def exitExpr_get_vertices(self, ctx:qlangParser.Expr_get_verticesContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_set_start.
    def enterExpr_set_start(self, ctx:qlangParser.Expr_set_startContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_set_start.
    def exitExpr_set_start(self, ctx:qlangParser.Expr_set_startContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_lambda.
    def enterExpr_lambda(self, ctx:qlangParser.Expr_lambdaContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_lambda.
    def exitExpr_lambda(self, ctx:qlangParser.Expr_lambdaContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_equal.
    def enterExpr_equal(self, ctx:qlangParser.Expr_equalContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_equal.
    def exitExpr_equal(self, ctx:qlangParser.Expr_equalContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_concat.
    def enterExpr_concat(self, ctx:qlangParser.Expr_concatContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_concat.
    def exitExpr_concat(self, ctx:qlangParser.Expr_concatContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_add_final.
    def enterExpr_add_final(self, ctx:qlangParser.Expr_add_finalContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_add_final.
    def exitExpr_add_final(self, ctx:qlangParser.Expr_add_finalContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_filter.
    def enterExpr_filter(self, ctx:qlangParser.Expr_filterContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_filter.
    def exitExpr_filter(self, ctx:qlangParser.Expr_filterContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_in.
    def enterExpr_in(self, ctx:qlangParser.Expr_inContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_in.
    def exitExpr_in(self, ctx:qlangParser.Expr_inContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_get_edge.
    def enterExpr_get_edge(self, ctx:qlangParser.Expr_get_edgeContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_get_edge.
    def exitExpr_get_edge(self, ctx:qlangParser.Expr_get_edgeContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_get_start.
    def enterExpr_get_start(self, ctx:qlangParser.Expr_get_startContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_get_start.
    def exitExpr_get_start(self, ctx:qlangParser.Expr_get_startContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_get_final.
    def enterExpr_get_final(self, ctx:qlangParser.Expr_get_finalContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_get_final.
    def exitExpr_get_final(self, ctx:qlangParser.Expr_get_finalContext):
        pass


    # Enter a parse tree produced by qlangParser#expr_get_labels.
    def enterExpr_get_labels(self, ctx:qlangParser.Expr_get_labelsContext):
        pass

    # Exit a parse tree produced by qlangParser#expr_get_labels.
    def exitExpr_get_labels(self, ctx:qlangParser.Expr_get_labelsContext):
        pass


    # Enter a parse tree produced by qlangParser#lambda.
    def enterLambda(self, ctx:qlangParser.LambdaContext):
        pass

    # Exit a parse tree produced by qlangParser#lambda.
    def exitLambda(self, ctx:qlangParser.LambdaContext):
        pass


    # Enter a parse tree produced by qlangParser#literal_string.
    def enterLiteral_string(self, ctx:qlangParser.Literal_stringContext):
        pass

    # Exit a parse tree produced by qlangParser#literal_string.
    def exitLiteral_string(self, ctx:qlangParser.Literal_stringContext):
        pass


    # Enter a parse tree produced by qlangParser#literal_int.
    def enterLiteral_int(self, ctx:qlangParser.Literal_intContext):
        pass

    # Exit a parse tree produced by qlangParser#literal_int.
    def exitLiteral_int(self, ctx:qlangParser.Literal_intContext):
        pass


    # Enter a parse tree produced by qlangParser#literal_list.
    def enterLiteral_list(self, ctx:qlangParser.Literal_listContext):
        pass

    # Exit a parse tree produced by qlangParser#literal_list.
    def exitLiteral_list(self, ctx:qlangParser.Literal_listContext):
        pass


    # Enter a parse tree produced by qlangParser#vertex.
    def enterVertex(self, ctx:qlangParser.VertexContext):
        pass

    # Exit a parse tree produced by qlangParser#vertex.
    def exitVertex(self, ctx:qlangParser.VertexContext):
        pass


    # Enter a parse tree produced by qlangParser#edge.
    def enterEdge(self, ctx:qlangParser.EdgeContext):
        pass

    # Exit a parse tree produced by qlangParser#edge.
    def exitEdge(self, ctx:qlangParser.EdgeContext):
        pass


    # Enter a parse tree produced by qlangParser#graph.
    def enterGraph(self, ctx:qlangParser.GraphContext):
        pass

    # Exit a parse tree produced by qlangParser#graph.
    def exitGraph(self, ctx:qlangParser.GraphContext):
        pass


    # Enter a parse tree produced by qlangParser#set.
    def enterSet(self, ctx:qlangParser.SetContext):
        pass

    # Exit a parse tree produced by qlangParser#set.
    def exitSet(self, ctx:qlangParser.SetContext):
        pass



del qlangParser