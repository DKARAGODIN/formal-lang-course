grammar qlang;

program: (stmt)* EOF;

stmt: (print | bind) SEMICOLON;

print: PRINT expr;
bind: var ASSIGN expr;


expr: LP expr RP
    | var
    | val
    | lambda
    | SET_START LP (list | expr) COMMA expr RP
    | SET_FINAL LP (list | expr) COMMA expr RP
    | ADD_START LP (list | expr) COMMA expr RP
    | ADD_FINAL LP (list | expr) COMMA expr RP
    | GET_START LP expr RP
    | GET_FINAL LP expr RP
    | GET_REACHABLE LP expr RP
    | GET_VERTICES LP expr RP
    | GET_EDGES LP expr RP
    | GET_LABELS LP expr RP
    | MAP LP lambda COMMA expr RP
    | FILTER LP lambda COMMA expr RP
    | LOAD LP string RP
    | expr INTERSECT expr
    | expr CONCAT expr
    | expr UNION expr
    | expr IN expr
    | expr EQUAL expr
    | expr NOT_EQUAL expr
    ;

lambda: lambda_def LP var RP ARROW LB expr RB;

lambda_def: 'lam';
var: CHAR*;

val:
    string
  | int
  | vertex
  | edge
  | graph
  | bool
  ;

bool: TRUE | FALSE;
string: QUOT (CHAR | DIGIT)* QUOT;
int: DIGIT+;
vertex: int;
edge: LP int COMMA string COMMA int RP;
graph: LP list COMMA list RP;
elem: string | int | vertex | edge | bool | var;
list: LB RB | LB elem ( COMMA elem )* RB;

DIGIT: [0-9];
CHAR: [a-zA-Z];

QUOT: '"';
EQUAL: '==';
NOT_EQUAL: '!=';
ASSIGN: '=';
PRINT: 'print';
TRUE: 'true';
FALSE: 'false';
SEMICOLON: ';';
COMMA: ',';
LP: '(';
RP: ')';
LB: '{';
RB: '}';

SET_START: 'setStart';
SET_FINAL: 'setFinal';
ADD_START: 'addStart';
ADD_FINAL: 'addFinal';
GET_START: 'getStart';
GET_FINAL: 'getFinal';
GET_REACHABLE: 'getReachable';
GET_VERTICES: 'getVertices';
GET_EDGES: 'getEdges';
GET_LABELS: 'getLabels';

MAP: 'map';
FILTER: 'filter';
LOAD: 'load';


KLEENE: '*';
ARROW: '->';
INTERSECT: '&';
CONCAT: '||';
UNION: '|';
IN: 'in';
COMMENT: '//' ~[\n]* -> skip;



