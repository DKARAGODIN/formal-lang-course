# Generated from project/qlang.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .qlangParser import qlangParser
else:
    from qlangParser import qlangParser

# This class defines a complete generic visitor for a parse tree produced by qlangParser.

class qlangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by qlangParser#program.
    def visitProgram(self, ctx:qlangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#stmt.
    def visitStmt(self, ctx:qlangParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#print.
    def visitPrint(self, ctx:qlangParser.PrintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#bind.
    def visitBind(self, ctx:qlangParser.BindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_set_final.
    def visitExpr_set_final(self, ctx:qlangParser.Expr_set_finalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_intersect.
    def visitExpr_intersect(self, ctx:qlangParser.Expr_intersectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_val.
    def visitExpr_val(self, ctx:qlangParser.Expr_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_not_equal.
    def visitExpr_not_equal(self, ctx:qlangParser.Expr_not_equalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_expr.
    def visitExpr_expr(self, ctx:qlangParser.Expr_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_map.
    def visitExpr_map(self, ctx:qlangParser.Expr_mapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_var.
    def visitExpr_var(self, ctx:qlangParser.Expr_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_add_start.
    def visitExpr_add_start(self, ctx:qlangParser.Expr_add_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_load.
    def visitExpr_load(self, ctx:qlangParser.Expr_loadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_get_reachable.
    def visitExpr_get_reachable(self, ctx:qlangParser.Expr_get_reachableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_get_vertices.
    def visitExpr_get_vertices(self, ctx:qlangParser.Expr_get_verticesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_set_start.
    def visitExpr_set_start(self, ctx:qlangParser.Expr_set_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_lambda.
    def visitExpr_lambda(self, ctx:qlangParser.Expr_lambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_equal.
    def visitExpr_equal(self, ctx:qlangParser.Expr_equalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_concat.
    def visitExpr_concat(self, ctx:qlangParser.Expr_concatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_add_final.
    def visitExpr_add_final(self, ctx:qlangParser.Expr_add_finalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_filter.
    def visitExpr_filter(self, ctx:qlangParser.Expr_filterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_in.
    def visitExpr_in(self, ctx:qlangParser.Expr_inContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_get_edge.
    def visitExpr_get_edge(self, ctx:qlangParser.Expr_get_edgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_get_start.
    def visitExpr_get_start(self, ctx:qlangParser.Expr_get_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_get_final.
    def visitExpr_get_final(self, ctx:qlangParser.Expr_get_finalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#expr_get_labels.
    def visitExpr_get_labels(self, ctx:qlangParser.Expr_get_labelsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#lambda.
    def visitLambda(self, ctx:qlangParser.LambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#literal_string.
    def visitLiteral_string(self, ctx:qlangParser.Literal_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#literal_int.
    def visitLiteral_int(self, ctx:qlangParser.Literal_intContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#literal_list.
    def visitLiteral_list(self, ctx:qlangParser.Literal_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#vertex.
    def visitVertex(self, ctx:qlangParser.VertexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#edge.
    def visitEdge(self, ctx:qlangParser.EdgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#graph.
    def visitGraph(self, ctx:qlangParser.GraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qlangParser#set.
    def visitSet(self, ctx:qlangParser.SetContext):
        return self.visitChildren(ctx)



del qlangParser