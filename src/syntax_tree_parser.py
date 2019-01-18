import ply.yacc as yacc
from node import Node, NodeValue, LeafValue

from ply_lex import tokens


def p_source(p):
    """source :
    | sourceItem"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[p[1]])


def p_sourceItem(p):
    """sourceItem :
    | funcDefs"""
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                    children=p[1])


def p_funcDefs(p):
    """funcDefs :
        | funcDef funcDefs
        | funcDef"""
    if len(p) == 1:
        p[0] = None
    if len(p) == 3:
        p[0] = [p[1], *p[2]] if type(p[2]) == list else [p[1], p[2]]
    if len(p) == 2:
        p[0] = p[1]


def p_funcDef(p):
    """funcDef : FUNCTION funcSignature statements END FUNCTION"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p),
                                info=NodeValue.set_info(p)),
                children=[p[2], p[3]])


def p_funcSignature(p):
    """funcSignature : identifier LBRACES argDefs RBRACES AS typeRef
                     | identifier LBRACES argDefs RBRACES"""
    expr_node = [p[1]]
    if p[3] is not None:
        expr_node += [*p[3]] if type(p[3]) == list else expr_node.append(p[3])
    if len(p) == 7:
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                    children=expr_node + [p[6]])
    else:
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                    children=expr_node)


def p_argDefs(p):
    """argDefs :
               | argDef COMMA argDefs
               | argDef"""
    if len(p) == 1:
        p[0] = None
    if len(p) == 4:
        p[0] = [p[1], *p[3]] if type(p[3]) == list else [p[1], p[3]]
    if len(p) == 2:
        p[0] = p[1]


def p_argDef(p):
    """argDef : identifier
              | identifier AS typeRef"""
    if len(p) == 4:
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), type=NodeValue.set_name(p)),
                    children=[p[1], p[3]])
    else:
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), type=NodeValue.set_name(p)),
                    children=[p[1]])


def p_typeRef(p):
    """typeRef : builtin
               | custom
               | array"""
    if type(p[1]) == Node:
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                    children=[p[1]])
    else:
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                    children=[p[1]])


def p_builtin(p):
    """builtin : BUILTIN_BOOL
               | BUILTIN_BYTE
               | BUILTIN_INT
               | BUILTIN_UINT
               | BUILTIN_LONG
               | BUILTIN_ULONG
               | BUILTIN_CHAR
               | BUILTIN_STRING
               | BUILTIN_LIST"""
    p[0] = Node(LeafValue(p, name=NodeValue.set_name(p)))


def p_custom(p):
    """custom : identifier"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[p[1]])


def p_array(p):
    """array : typeRef LBRACES commas RBRACES"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[p[1]])


def p_commas(p):
    """commas :
              | commas COMMA
              | COMMA"""


def p_identifiers(p):
    """identifiers : identifier COMMA identifiers
                   | identifier"""
    if len(p) == 1:
        p[0] = None
    if len(p) == 4:
        p[0] = [p[1], *p[3]] if type(p[3]) == list else [p[1], p[3]]
    if len(p) == 2:
        p[0] = [p[1]]


def p_identifier(p):
    """identifier : IDENTIFIER"""
    p[0] = Node(LeafValue(p, name=NodeValue.set_name(p)))


def p_statements(p):
    """statements : pre_statements
    """
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=p[1]) if p[1] else None


def p_statement_nodes(p):
    """pre_statements :
                      | statement pre_statements
                      | statement
    """
    if len(p) == 1:
        p[0] = []
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = [p[1], *p[2]] if type(p[2]) == list else [p[1], p[2]]


def p_statement(p):
    """statement : var
                 | if
                 | while
                 | do
                 | break
                 | expression"""
    p[0] = p[1]


def p_var(p):
    """var : DIM identifiers AS typeRef"""
    p[4].value.set_type(p[3])
    names = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p), type=p[1]),
                 children=[*p[2]])

    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p)),
                children=[names, p[4]])


def p_if(p):
    """if : IF expr THEN statements END IF
          | IF expr THEN statements ELSE statements END IF"""
    p[2].value.set_type(p[1])
    p[4].value.set_type(p[3])
    if len(p) == 7:
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p)),
                    children=[p[2], p[4]])
    else:
        p[6].value.set_type(p[5])
        p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p)),
                    children=[p[2], p[4], p[6]])


def p_while(p):
    """while : WHILE expr statements WEND"""
    p[2].value.set_type(p[1])
    p[3].value.set_type('do')
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p)),
                children=[p[2], p[3]])


def p_do(p):
    """do : DO statements LOOP WHILE expr
          | DO statements LOOP UNTIL expr"""
    p[2].value.set_type(p[1])
    p[5].value.set_type(p[4])
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p)),
                children=[p[2], p[5]])


def p_break(p):
    """break : BREAK"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p)))


def p_expression(p):
    """expression : expr SEMICOLON"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p)), children=[p[1]])


def p_exprs(p):
    """exprs :
             | expr COMMA exprs
             | expr
    """
    if len(p) == 1:
        p[0] = None
    if len(p) == 4:
        p[0] = [p[1], *p[3]] if type(p[3]) == list else [p[1], p[3]]
    if len(p) == 2:
        p[0] = p[1]


def p_expr(p):
    """expr : binary
            | assignment
            | unary
            | braces
            | callOrIndexer
            | place
            | literal
    """
    p[0] = p[1]


def p_binary(p):
    """binary : expr PLUS expr
              | expr MINUS expr
              | expr DIVIDE expr
              | expr MUL expr
              | expr LESS_EQ expr
              | expr MORE_EQ expr
              | expr MORE expr
              | expr NOT_EQ expr
              | expr EQUAL expr
              | expr AND expr
              | expr OR expr
    """
    node = Node(value=NodeValue(name=p[2]),
                children=[p[1], p[3]])
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p),
                                info=NodeValue.set_info(p, pos=2)),
                children=[node])


def p_unary(p):
    """unary : NOT expr
             | MINUS expr
    """
    node = Node(value=NodeValue(name=p[1]),
                children=[p[2]])
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[node])


def p_assignment(p):
    """assignment : identifiers ASSIGNMENT expr
    """
    p[3].value.set_type(p[2])
    names = Node(value=NodeValue(name='identifiers', info=NodeValue.set_info(p)),
                 children=[*p[1]])

    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p, pos=2)),
                children=[names, p[3]])


def p_braces(p):
    """braces : LBRACES expr RBRACES"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[p[2]])


def p_callOrIndexer(p):
    """callOrIndexer : expr LBRACES exprs RBRACES"""
    p[1].value.set_type('Left')
    exprs_node = []
    if type(p[3]) == list:
        exprs_node += [*p[3]]
    else:
        exprs_node.append(p[3])
    args = Node(value=NodeValue(name=NodeValue.set_name(p), info=NodeValue.set_info(p), type='In brace'),
                children=exprs_node)

    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p),
                                info=NodeValue.set_info(p, pos=2)),
                children=[p[1], args])


def p_place(p):
    """place : identifier"""
    p[0] = p[1]


def p_literal(p):
    """literal : bool
               | str
               | char
               | hex
               | bits
               | dec"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[p[1]])


def p_str(p):
    """str : STR"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[Node(LeafValue(p, name=NodeValue.set_name(p), replace='"'))])


def p_char(p):
    """char : CHAR"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[Node(LeafValue(p, name=NodeValue.set_name(p), replace='\''))])


def p_hex(p):
    """hex : HEX"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[Node(LeafValue(p, name=NodeValue.set_name(p)))])


def p_bits(p):
    """bits : BITS"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[Node(LeafValue(p, name=NodeValue.set_name(p)))])


def p_dec(p):
    """dec : DEC"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[Node(LeafValue(p, name=NodeValue.set_name(p)))])


def p_bool(p):
    """bool : BOOL"""
    p[0] = Node(value=NodeValue(name=NodeValue.set_name(p)),
                children=[Node(LeafValue(p, name=NodeValue.set_name(p)))])


def p_error(p):
    print('Unexpected token:', p)


parser = yacc.yacc(debug=True)


def parse_tokens(path):
    with open(path) as file_handler:
        input_file = file_handler.read()
        root = parser.parse(input_file)
        root.value.name = path
    return root
