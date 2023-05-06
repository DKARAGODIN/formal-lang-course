# Язык запросов к графам

## Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Set of set
  | List of list

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda = List<var> * expr
```

## Описание конкретного синтаксиса языка

Синтаксис старался сделать максимально похожим на java.

```
grammar language;

program: (stmt)* EOF;

stmt: (PRINT | BIND) SEMICOLON;
print: print expr;
bind: VAR ASSIGN expr;

String: STRING
Int: DIGIT+
Vertex: INT
Edge: LP INT COMMA STRING RP
Graph: LP LIST COMMA LIST RP
Bool: BOOL

val:
    String
  | Int
  | Vertex
  | Edge
  | Graph
  | Bool

expr: LP expr RP
    | var
    | val
    | SET_START LP (LIST | expr) COMMA expr RP
    | SET_FINAL LP (LIST | expr) COMMA expr RP
    | ADD_START LP (LIST | expr) COMMA expr RP
    | ADD_FINAL LP (LIST | expr) COMMA expr RP
    | GET_START LP expr RP
    | GET_FINAL LP expr RP
    | GET_REACHABLE LP expr RP
    | GET_VERTICES LP expr RP
    | GET_EDGES LP expr RP
    | GET_LABELS LP expr RP
    | MAP LP lambda COMMA expr RP
    | FILTER LP lambda COMMA expr RP
    | LOAD LP STRING RP
    | expr INTERSECT expr
    | expr CONCAT expr
    | expr UNION expr
    | expr IN expr
    | expr EQUAL expr
    | expr NOT_EQUAL expr

lambda: LP LIST RP ARROW LB expr RB

COMMA: ','
ASSIGN: '='
EQUAL: '=='
NOT_EQUAL: '!='
QUOT: '"'
SEMICOLON: ';'
LP: '('
RP: ')'
LB: '{'
RB: '}'
PRINT: 'print'
BOOL: 'true' | 'false'

SET_START: 'setStart'
SET_FINAL: 'setFinal'
ADD_START: 'addStart'
ADD_FINAL: 'addFinal'
GET_START: 'getStart'
GET_FINAL: 'getFinal'
GET_REACHABLE: 'getReachable'
GET_VERTICES: 'getVertices'
GET_EDGES: 'getEdges'
GET_LABELS: 'getLabels'
LOAD: 'load'
MAP: 'map'
FILTER: 'filter'

KLEENE: '*'
ARROW: '->'
TRUE: 'true'
FALSE: 'false'
DIGIT: [0-9]
CHAR: [a-zA-Z]
VAR: CHAR*
STRING: QUOT (CHAR | DIGIT)* QUOT
ELEM: BOOL | DIGIT | CHAR | STRING | vertex | edge
LIST: LB RB | LB ELEM ( COMMA ELEM )* RB

INTERSECT: '&'
CONCAT: '||'
UNION: '|'
IN: 'in'

COMMENT: '//'
```
## Пример запроса в этом синтаксисе
```
//Пример комментария
g = load("./test/graph");
start = 1;
newG = setStart(start , g)
list = {2,3};
anotherG = setFinal(list, newG);
reachable = getReachable(anotherG);
edges = getEdges(g);
u = filter(( v ) -> {v == start}, reachable);
b = filter(( v ) -> {v != start}, reachable);
a = u & b;
print a;
```