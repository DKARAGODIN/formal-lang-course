from enum import Enum
from typing import Iterable

from antlr4 import *
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol

from dist.qlangLexer import qlangLexer
from dist.qlangParser import qlangParser
from dist.qlangVisitor import qlangVisitor
from project.g_util import read_graph_from_file, load_graph
from project.matrix_util import AdjacencyMatrix, intersect_adjacency_matrices, adjacency_matrix_to_nfa, iterate_nfa, \
    concat
from project.regex_util import graph_to_nfa, regex_string_to_min_dfa


class ValueType(Enum):
    StringValue = 1
    IntValue = 2
    SetValue = 3
    FiniteAutomataValue = 4
    RSMValue = 5
    BoolValue = 6


class ValueHolder:
    def __init__(self, value, ctx, value_type = ValueType.StringValue):
        self.value = value
        self.ctx = ctx
        self.value_type = value_type

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, ValueHolder):
            return self.value_type == other.value_type and self.value == other.value
        else:
            return False


def interpret(program: ParserRuleContext, out=None):
    visitor = InterpretVisitor(out=out)
    try:
        return program.accept(visitor)

    except Exception as e:
        raise InterpretError(e, visitor.ctx) from e


class InterpretVisitor(qlangVisitor):
    def __init__(self, out=None):
        self.ctx_stack = list()
        self.scopes = [dict()]
        self.out = out

    def enter_ctx(self, ctx: ParserRuleContext):
        self.ctx_stack.append(ctx)

    def exit_ctx(self):
        self.ctx_stack.pop()

    def get_nfa_from_holder(self, holder: ValueHolder, ctx) -> ValueHolder:
        if holder.value_type is ValueType.FiniteAutomataValue:
            return holder
        elif holder.value_type is ValueType.StringValue:
            casted_value = regex_string_to_min_dfa(holder.value)
            result = ValueHolder(value=casted_value, ctx=ctx, value_type=ValueType.FiniteAutomataValue)
            return result
        else:
            raise InterpretError("Can not create NFA from " + str(holder.value_type) + " type")

    def add_starts(self, to: ValueHolder, starts: ValueHolder, ctx) -> ValueHolder:
        if to.value_type is ValueType.FiniteAutomataValue:
            to_nfa = to.value
        elif to.value_type is ValueType.StringValue:
            to_nfa = regex_string_to_min_dfa(to.value)
        else:
            raise InterpretError("Can not create NFA from " + str(to.value_type) + " type")

        if starts.value_type is ValueType.SetValue:
            starts_set = starts.value
        else:
            raise InterpretError("Can not set starts from " + str(to.value_type) + " type")

        for node in starts_set:
            to_nfa.add_start_state(node)

        result = ValueHolder(value=to_nfa, ctx=ctx, value_type=ValueType.FiniteAutomataValue)
        return result

    def add_finals(self, to: ValueHolder, starts: ValueHolder, ctx) -> ValueHolder:
        if to.value_type is ValueType.FiniteAutomataValue:
            to_nfa = to.value
        elif to.value_type is ValueType.StringValue:
            to_nfa = regex_string_to_min_dfa(to.value)
        else:
            raise InterpretError("Can not create NFA from " + str(to.value_type) + " type")

        if starts.value_type is ValueType.SetValue:
            starts_set = starts.value
        else:
            raise InterpretError("Can not set starts from " + str(to.value_type) + " type")

        for node in starts_set:
            to_nfa.add_final_state(node)

        result = ValueHolder(value=to_nfa, ctx=ctx, value_type=ValueType.FiniteAutomataValue)
        return result

    def set_starts(self, to: ValueHolder, starts: ValueHolder, ctx) -> ValueHolder:
        if to.value_type is ValueType.FiniteAutomataValue:
            to_nfa = to.value
        elif to.value_type is ValueType.StringValue:
            to_nfa = regex_string_to_min_dfa(to.value)
        else:
            raise InterpretError("Can not create NFA from " + str(to.value_type) + " type")

        if starts.value_type is ValueType.SetValue:
            starts_set = starts.value
        else:
            raise InterpretError("Can not set starts from " + str(to.value_type) + " type")

        old_starts = to_nfa.start_states
        old_starts.clear()
        for node in starts_set:
            to_nfa.add_start_state(node)

        result = ValueHolder(value=to_nfa, ctx=ctx, value_type=ValueType.FiniteAutomataValue)
        return result

    def set_finals(self, to: ValueHolder, starts: ValueHolder, ctx) -> ValueHolder:
        if to.value_type is ValueType.FiniteAutomataValue:
            to_nfa = to.value
        elif to.value_type is ValueType.StringValue:
            to_nfa = regex_string_to_min_dfa(to.value)
        else:
            raise InterpretError("Can not create NFA from " + str(to.value_type) + " type")

        if starts.value_type is ValueType.SetValue:
            starts_set = starts.value
        else:
            raise InterpretError("Can not set starts from " + str(to.value_type) + " type")

        old_starts = to_nfa.final_states
        old_starts.clear()
        for node in starts_set:
            to_nfa.add_final_state(node)

        result = ValueHolder(value=to_nfa, ctx=ctx, value_type=ValueType.FiniteAutomataValue)
        return result

    def get_reachable(self, value:ValueHolder, ctx) -> ValueHolder:
        if value.value_type is ValueType.StringValue:
            dfa = regex_string_to_min_dfa(value.value)
        reachables = dfa._get_reachable_states()
        result = ValueHolder(value=reachables, ctx=ctx, value_type=ValueType.SetValue)
        return result

    def get_verices(self, value:ValueHolder, ctx) -> ValueHolder:
        if value.value_type is ValueType.StringValue:
            dfa = regex_string_to_min_dfa(value.value)
        reachables = dfa.states
        result = ValueHolder(value=reachables, ctx=ctx, value_type=ValueType.SetValue)
        return result

    def get_edges(self, value:ValueHolder, ctx) -> ValueHolder:
        if value.value_type is ValueType.StringValue:
            dfa = regex_string_to_min_dfa(value.value)
        it = iterate_nfa(dfa)
        edges = {(u, l, v) for u, l, v in it}
        result = ValueHolder(value=edges, ctx=ctx, value_type=ValueType.SetValue)
        return result

    def get_labels(self, value:ValueHolder, ctx) -> ValueHolder:
        if value.value_type is ValueType.StringValue:
            dfa = regex_string_to_min_dfa(value.value)
        labels = dfa.symbols
        result = ValueHolder(value=labels, ctx=ctx, value_type=ValueType.SetValue)
        return result

    def compare_value_holders(self, left:ValueHolder, right:ValueHolder, ctx) -> ValueHolder:
        if left.value_type is not right.value_type:
            raise InterpretError("Incomparable value types: " + str(left.value_type) + " and " + str(right.value_type))
        result = left.value == right.value
        return ValueHolder(value=result, ctx=ctx, value_type=ValueType.BoolValue)

    def contains_value(self, left:ValueHolder, right:ValueHolder, ctx) -> ValueHolder:
        if right.value_type is not ValueType.SetValue:
            raise InterpretError("Operator In is not supported by type " + str(right.value_type))

        container = right.value
        result = left.value in container
        return ValueHolder(value=result, ctx=ctx, value_type=ValueType.BoolValue)

    def intersect_value_holders(self, left:ValueHolder, right:ValueHolder, ctx) -> ValueHolder:
        if left.value_type is not right.value_type:
            raise InterpretError("Incomparable value types: " + str(left.value_type) + " and " + str(right.value_type))

        if left.value_type is ValueType.BoolValue:
            result = left.value and right.value_type
            result = ValueHolder(value=result, ctx=ctx, value_type=ValueType.BoolValue)
        elif left.value_type is ValueType.SetValue:
            result = left.value.union(right.value)
            result = ValueHolder(value=result, ctx=ctx, value_type=ValueType.SetValue)
        elif left.value_type is ValueType.FiniteAutomataValue:
            intersection_am = intersect_adjacency_matrices(AdjacencyMatrix(left.value), AdjacencyMatrix(right.value))
            intersection = adjacency_matrix_to_nfa(intersection_am)
            result = ValueHolder(value=intersection, ctx=ctx, value_type=ValueType.FiniteAutomataValue)
        else:
            raise InterpretError("Unsupported operation & for type " + str(left.value_type))

        return result

    def concat_value_holders(self, left:ValueHolder, right:ValueHolder, ctx) -> ValueHolder:
        if left.value_type is not right.value_type:
            raise InterpretError("Incomparable value types: " + str(left.value_type) + " and " + str(right.value_type))

        if left.value_type is ValueType.BoolValue:
            result = left.value or right.value_type
            result = ValueHolder(value=result, ctx=ctx, value_type=ValueType.BoolValue)
        elif left.value_type is ValueType.StringValue:
            result = left.value + right.value
            result = ValueHolder(value=result, ctx=ctx, value_type=ValueType.StringValue)
        elif left.value_type is ValueType.SetValue:
            result = left.value.intersection(right.value)
            result = ValueHolder(value=result, ctx=ctx, value_type=ValueType.SetValue)
        elif left.value_type is ValueType.FiniteAutomataValue:
            result = concat(left.value, right.value)
            result = ValueHolder(value=result, ctx=ctx, value_type=ValueType.StringValue)
        else:
            raise InterpretError("Unsupported operation || for type " + str(left.value_type))
        return result

    @property
    def ctx(self) -> ParserRuleContext:
        if len(self.ctx_stack) == 0:
            return None
        return self.ctx_stack[-1]

    @property
    def scope(self) -> dict[str, ValueHolder]:
        return self.scopes[-1]

    def return_value_from_scope(self, name: str) -> ValueHolder:
        try:
            return self.scope[name]
        except KeyError as e:
            raise ValueError(f'name "{str}" is not in scope') from e

    def visitProgram(self, ctx: qlangParser.ProgramContext):
        self.enter_ctx(ctx)
        stmts = ctx.stmt()
        for stmt in stmts:
            stmt.accept(self)
        self.exit_ctx()

    def visitExpr_expr(self, ctx:qlangParser.Expr_exprContext):
        self.enter_ctx(self)
        value = ctx.children[1].accept(self)
        self.exit_ctx()
        return value

    def visitExpr_load(self, ctx:qlangParser.Expr_loadContext):
        self.enter_ctx(ctx)
        g = graph_to_nfa(load_graph(eval(ctx.value.text)))
        result = ValueHolder(value=g, ctx=ctx, value_type=ValueType.FiniteAutomataValue)
        self.exit_ctx()
        return result

    def visitBind(self, ctx:qlangParser.BindContext):
        self.enter_ctx(ctx)
        value = ctx.value.accept(self)
        self.scopes[0][ctx.name.text] = value
        self.exit_ctx()

    def visitPrint(self, ctx:qlangParser.PrintContext):
        self.enter_ctx(ctx)
        print(repr(ctx.value.accept(self)), file=self.out)
        self.exit_ctx()

    def visitExpr_val(self, ctx:qlangParser.Expr_valContext):
        self.enter_ctx(ctx)
        #only one child possible - either string or int
        val = ctx.children[0].accept(self)
        self.exit_ctx()
        return val

    def visitExpr_var(self, ctx:qlangParser.Expr_valContext):
        self.enter_ctx(ctx)
        result = self.return_value_from_scope(ctx.name.text)
        self.exit_ctx()
        return result

    def visitLiteral_string(self, ctx:qlangParser.Literal_stringContext):
        self.enter_ctx(ctx)
        s = ValueHolder(value=eval(ctx.value.text), ctx=ctx, value_type=ValueType.StringValue)
        self.exit_ctx()
        return s

    def visitLiteral_int(self, ctx:qlangParser.Literal_stringContext):
        self.enter_ctx(ctx)
        i = ValueHolder(value=eval(ctx.value.text), ctx=ctx, value_type=ValueType.IntValue)
        self.exit_ctx()
        return i

    def visitLiteral_list(self, ctx:qlangParser.Literal_listContext):
        self.enter_ctx(ctx)
        try:
            if len(ctx.children[0].children) == 2:
                s = ValueHolder({}, ctx, ValueType.SetValue)
            else:
                v = set()
                for x in ctx.children[0].elems:
                    v.add(x.accept(self).value)
                s = ValueHolder(value=v, ctx=ctx, value_type=ValueType.SetValue)
        except:
            raise InterpretError("Invalid set declaration")
        self.exit_ctx()
        return s

    def visitExpr_lambda(self, ctx:qlangParser.Expr_lambdaContext):
        self.enter_ctx(self)
        self.exit_ctx()

    def visitExpr_map(self, ctx:qlangParser.Expr_mapContext):
        self.enter_ctx(ctx)
        self.exit_ctx()

    def visitExpr_filter(self, ctx:qlangParser.Expr_filterContext):
        self.enter_ctx(ctx)
        self.exit_ctx()

    def visitExpr_add_start(self, ctx:qlangParser.Expr_set_startContext):
        self.enter_ctx(ctx)
        to = ctx.to.accept(self)
        starts = ctx.start.accept(self)
        result = self.add_starts(to, starts, ctx)
        self.exit_ctx()
        return result

    def visitExpr_add_final(self, ctx:qlangParser.Expr_set_finalContext):
        self.enter_ctx(ctx)
        to = ctx.to.accept(self)
        finals = ctx.final.accept(self)
        result = self.add_finals(to, finals, ctx)
        self.exit_ctx()
        return result

    def visitExpr_set_start(self, ctx:qlangParser.Expr_set_startContext):
        self.enter_ctx(ctx)
        to = ctx.to.accept(self)
        starts = ctx.start.accept(self)
        result = self.set_starts(to, starts, ctx)
        self.exit_ctx()
        return result

    def visitExpr_set_final(self, ctx:qlangParser.Expr_set_finalContext):
        self.enter_ctx(ctx)
        to = ctx.to.accept(self)
        finals = ctx.final.accept(self)
        result = self.set_finals(to, finals, ctx)
        self.exit_ctx()
        return result

    def visitExpr_get_start(self, ctx:qlangParser.Expr_get_startContext):
        self.enter_ctx(ctx)
        value = ctx.value.accept(self)
        dfa = self.get_nfa_from_holder(value, ctx)
        result = ValueHolder(value=dfa.value.start_states, ctx=ctx, value_type=ValueType.SetValue)
        self.exit_ctx()
        return result

    def visitExpr_get_final(self, ctx:qlangParser.Expr_get_finalContext):
        self.enter_ctx(ctx)
        value = ctx.value.accept(self)
        dfa = self.get_nfa_from_holder(value, ctx)
        result = ValueHolder(value=dfa.value.final_states, ctx=ctx, value_type=ValueType.SetValue)
        self.exit_ctx()
        return result

    def visitExpr_get_reachable(self, ctx:qlangParser.Expr_get_reachableContext):
        self.enter_ctx(ctx)
        value = ctx.value.accept(self)
        result = self.get_reachable(value, ctx)
        self.exit_ctx()
        return result

    def visitExpr_get_vertices(self, ctx:qlangParser.Expr_get_verticesContext):
        self.enter_ctx(ctx)
        value = ctx.value.accept(self)
        result = self.get_verices(value, ctx)
        self.exit_ctx()
        return result

    def visitExpr_get_edge(self, ctx:qlangParser.Expr_get_edgeContext):
        self.enter_ctx(ctx)
        value = ctx.value.accept(self)
        result = self.get_edges(value, ctx)
        self.exit_ctx()
        return result

    def visitExpr_get_labels(self, ctx:qlangParser.Expr_get_labelsContext):
        self.enter_ctx(ctx)
        value = ctx.value.accept(self)
        result = self.get_labels(value, ctx)
        self.exit_ctx()
        return result

    def visitExpr_equal(self, ctx:qlangParser.Expr_equalContext):
        self.enter_ctx(ctx)
        left_value = ctx.left.accept(self)
        right_value = ctx.right.accept(self)
        result = self.compare_value_holders(left_value, right_value, ctx)
        self.exit_ctx()
        return result

    def visitExpr_not_equal(self, ctx:qlangParser.Expr_not_equalContext):
        self.enter_ctx(ctx)
        left_value = ctx.left.accept(self)
        right_value = ctx.right.accept(self)
        result = self.compare_value_holders(left_value, right_value, ctx)
        result = ValueHolder(value=not result.value, ctx=ctx, value_type=ValueType.BoolValue)
        self.exit_ctx()
        return result

    def visitExpr_in(self, ctx:qlangParser.Expr_inContext):
        self.enter_ctx(ctx)
        left_value = ctx.left.accept(self)
        right_value = ctx.right.accept(self)
        result = self.contains_value(left_value, right_value, ctx)
        self.exit_ctx()
        return result

    def visitExpr_intersect(self, ctx:qlangParser.Expr_intersectContext):
        self.enter_ctx(ctx)
        left_value = ctx.left.accept(self)
        right_value = ctx.right.accept(self)
        result = self.intersect_value_holders(left_value, right_value, ctx)
        self.exit_ctx()
        return result

    def visitExpr_concat(self, ctx:qlangParser.Expr_concatContext):
        self.enter_ctx(ctx)
        left_value = ctx.left.accept(self)
        right_value = ctx.right.accept(self)
        result = self.concat_value_holders(left_value, right_value, ctx)
        self.exit_ctx()
        return result

def ctx_location(ctx: ParserRuleContext) -> str:
    return f"{ctx.start.line}:{ctx.start.column + 1}"


class InterpretError(Exception):
    def __init__(self, ex, ctx):
        self.ex = ex
        self.ctx = ctx

    def __str__(self):
        if self.ctx is None:
            return str(self.ex)
        return f"{ctx_location(self.ctx)}: {self.ex}"
