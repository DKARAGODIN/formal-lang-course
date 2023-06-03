grammar qlang;

fragment W: [a-zA-Z_];
fragment D: [0-9];
fragment WD: (W|D);
fragment S: [ \t\r\n\u000C];

INT_NUMBER: [1-9][0-9]*|'0';
STRING: '"' ('\\'. | (~'"')+)* '"';
NAME: W WD*;
WS: S+ -> skip;

program: (stmt)* EOF;
stmt: (print | bind) ';';
print: 'print' value=expr;
bind: 'bind' name=NAME '=' value=expr;

expr: '(' expr ')'                               # expr_expr
    | name=NAME                                  # expr_var
    | val                                        # expr_val
    | lambda                                     # expr_lambda
    | 'setStart' '(' to=expr ',' start=expr ')'  # expr_set_start
    | 'setFinal' '(' to=expr ',' final=expr ')'  # expr_set_final
    | 'addStart' '(' to=expr ',' start=expr ')'  # expr_add_start
    | 'addFinal' '(' to=expr ',' final=expr ')'  # expr_add_final
    | 'getStart' '(' value=expr ')'              # expr_get_start
    | 'getFinal' '(' value=expr ')'              # expr_get_final
    | 'getReachable' '(' value=expr ')'          # expr_get_reachable
    | 'getVertices' '(' value=expr ')'           # expr_get_vertices
    | 'getEdges' '(' value=expr ')'              # expr_get_edge
    | 'getLabels' '(' value=expr ')'              # expr_get_labels
    | 'map' '(' lambda ',' expr ')'               # expr_map
    | 'filter' '(' lambda ',' expr ')'            # expr_filter
    | 'load' '(' value=STRING ')'                 # expr_load
    | left=expr '&&' right=expr                   # expr_intersect
    | left=expr '||' right=expr                   # expr_concat
    | left=expr 'in' right=expr                   # expr_in
    | left=expr '==' right=expr                   # expr_equal
    | left=expr '!=' right=expr                   # expr_not_equal
    ;

lambda: 'lam' '(' var=NAME ')' '->' '{' body=expr '}';

val:
    value=STRING # literal_string
  | value=INT_NUMBER # literal_int
  | set # literal_list
  ;

vertex: INT_NUMBER;
edge: '(' INT_NUMBER ',' STRING ',' INT_NUMBER ')';
graph: '(' set ',' set ')';
set: '{' '}' | '{' elems+=expr ( ',' elems+=expr )* '}';

COMMENT: '//' ~[\n]* -> skip;
