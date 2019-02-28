from language import *
from node import NodeValue

import ply.yacc as yacc
from ply_lex import tokens

precedence = (('nonassoc', 'LESS_EQ', 'LESS', 'MORE_EQ', 'MORE', 'NOT_EQ', 'EQUAL'),
              ('left', 'PLUS', 'MINUS', 'OR'),
              ('left', 'DIVIDE', 'MUL', 'AND'),
              ('right', 'NOT', 'UMINUS'))

def set_pos(p, index):
    line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos(index)) + 1
    return {'line': (p.lineno(index)),
            'pos': (p.lexpos(index) - line_start) + 1}


def add_to_list(l, obj):
    l.extend(obj) if type(obj) == list else l.append(obj)
    return [i for i in l if i is not None]


def p_source(p):
    """source :
    | sourceItem"""
    try:
        p[0] = Source(children=[*p[1]])
    except IndexError:
        p[0] = Source()


def p_sourceItem(p):
    """sourceItem :
                  | funcDef sourceItem"""
    if len(p) == 1:
        p[0] = None
    if len(p) == 3:
        p[0] = []
        p[0] = add_to_list(p[0], p[1])
        p[0] = add_to_list(p[0], p[2])


def p_funcDef(p):
    """funcDef : FUNCTION funcSignature statements END FUNCTION"""
    stmts = NodeValue(role='statements', children=p[3])
    p[0] = Function(signature=p[2], statements=p[3], pos=set_pos(p, 1), children=[p[2], stmts])


def p_funcSignature(p):
    """funcSignature : identifier LBRACES argDefs RBRACES AS typeRef
                     | identifier LBRACES argDefs RBRACES"""
    identifier = NodeValue(role='identifier', children=[p[1]])
    argDefs = NodeValue(role='argDefs', children=p[3])
    if len(p) == 7:
        typeRef = NodeValue(role='typeRef', children=p[3])
        p[0] = FuncSignature(name=p[1].name, args=p[3], pos=set_pos(p, 1), func_type=p[6], children=[identifier, argDefs, typeRef])
    else:
        p[0] = FuncSignature(name=p[1].name, args=p[3], pos=set_pos(p, 1), children=[identifier, argDefs])


def p_argDefs(p):
    """argDefs :
               | argDef
               | argDef COMMA argDefs"""
    if len(p) == 1:
        p[0] = []
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 4:
        p[0] = []
        p[0] = add_to_list(p[0], p[1])
        p[0] = add_to_list(p[0], p[3])
        if not p[0]:
            p[0] = []


def p_argDef(p):
    """argDef : identifier
              | identifier AS typeRef"""
    identifier = NodeValue(role='identifier', children=[p[1]])
    if len(p) == 4:
        typeRef = NodeValue(role='typeRef', children=[p[3]])
        p[0] = Argument(identifier=p[1], expected_type=p[3], children=[typeRef, identifier])
    else:
        p[0] = Argument(identifier=p[1], children=[identifier])


def p_typeRef(p):
    """typeRef : builtin
               | custom
               | array"""
    p[0] = p[1]


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
    p[0] = NodeValue(role=p[1], pos=set_pos(p, 1))


def p_custom(p):
    """custom : identifier"""
    p[0] = NodeValue(role=p[1].value, pos=set_pos(p, 1))


def p_array(p):
    """array : typeRef LBRACES commas RBRACES"""
    p[0] = Array(type=p[1], len=p[3])


def p_commas(p):
    """commas :
              | commas COMMA"""
    if len(p) == 1:
        p[0] = 0
    if len(p) == 3:
        p[0] = p[1] + 1


def p_identifiers(p):
    """identifiers : identifier COMMA identifiers
                   | identifier"""
    if len(p) == 2:
        p[0] = []
        p[0] = add_to_list(p[0], p[1])
    if len(p) == 4:
        p[0] = []
        p[0] = add_to_list(p[0], p[1])
        p[0] = add_to_list(p[0], p[3])


def p_identifier(p):
    """identifier : IDENTIFIER"""
    p[0] = Identifier(name=p[1], type=p.slice[0].type, pos=set_pos(p, 1))


def p_statements(p):
    """statements :
                  | statement statements
    """
    if len(p) == 1:
        p[0] = None
    if len(p) == 3:
        p[0] = []
        p[0] = add_to_list(p[0], p[1])
        p[0] = add_to_list(p[0], p[2])


def p_statement(p):
    """statement : var
                 | if
                 | while
                 | do
                 | break
                 | expression
                 | assignment SEMICOLON"""
    p[0] = p[1]


def p_var(p):
    """var : DIM identifiers AS typeRef"""
    names = NodeValue(role='names', children=[NodeValue(role=str(p[2]))])
    type = NodeValue(role='type', children=[p[4]])
    dim = NodeValue(role='dim', children=[names, type])
    p[0] = Declaration(identifiers=p[2], type=p[4], pos=set_pos(p, 1), children=[dim])


def p_if(p):
    """if : IF expr THEN statements END IF
          | IF expr THEN statements ELSE statements END IF"""
    _if = NodeValue(role='if', children=[p[2]])
    _then = NodeValue(role='then', children=[*p[4]])
    if len(p) == 7:
        p[0] = If(expr=p[2], then_stmt=p[4], pos=set_pos(p, 1), children=[_if, _then])
    else:
        _else = NodeValue(role='else', children=[*p[6]])
        p[0] = If(expr=p[2], then_stmt=p[4], else_stmt=p[6], pos=set_pos(p, 1), children=[_if, _then, _else])


def p_while(p):
    """while : WHILE expr statements WEND"""
    _while = NodeValue(role='while', children=[p[2]])
    _do = NodeValue(role='do', children=[*p[3]])
    p[0] = While(expr=p[2], do_stmt=p[3], pos=set_pos(p, 1), children=[_while, _do])


def p_do(p):
    """do : DO statements LOOP WHILE expr
          | DO statements LOOP UNTIL expr"""
    _loop = NodeValue(role=p[4], children=[p[5]])
    _do = NodeValue(role='do', children=[*p[2]])
    p[0] = While(expr=p[5], do_stmt=p[2], loop_type=p[4], pos=set_pos(p, 1), children=[_do, _loop])


def p_break(p):
    """break : BREAK"""
    p[0] = Break(pos=set_pos(p, 1))


def p_expression(p):
    """expression : expr SEMICOLON"""
    expression = NodeValue(role='expression', children=[p[1]])
    p[0] = Expression(expr=p[1], pos=set_pos(p, 2), children=[expression])


def p_exprs(p):
    """exprs :
             | expr
             | expr COMMA exprs
    """
    if len(p) == 1:
        p[0] = None
    if len(p) == 2:
        p[0] = []
        p[0] = add_to_list(p[0], p[1])
    if len(p) == 4:
        p[0] = []
        p[0] = add_to_list(p[0], p[1])
        p[0] = add_to_list(p[0], p[3])
        if not p[0]:
            p[0] = []


def p_expr(p):
    """expr : binary
            | unary
            | braces
            | callOrIndexer
            | index
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
    binary = NodeValue(role=p[2], children=[p[1], p[3]])
    p[0] = BinaryExpression(left=p[1], right=p[3], operand=p[2], children=[binary])


def p_unary(p):
    """unary : NOT expr
             | MINUS expr %prec UMINUS
    """
    unary = NodeValue(role=p[1], children=[p[2]])
    p[0] = UnaryExpression(expr=p[2], operand=p[1], children=[unary])


def p_assignment(p):
    """assignment : identifiers ASSIGNMENT expr
    """
    identifiers = NodeValue(role='identifiers', children=[NodeValue(role=str(p[1]))])
    value = NodeValue(role='value', children=[p[3]])
    assignment = NodeValue(role='assignment', children=[identifiers, value])
    p[0] = Assignment(p[1], p[3], pos=set_pos(p, 2), children=[assignment])


def p_braces(p):
    """braces : LBRACES expr RBRACES"""
    braces = NodeValue(role='braces', children=[p[2]])
    p[0] = Brace(expr=p[2], pos=set_pos(p, 1), brace=True, children=[braces])


def p_callOrIndexer(p):
    """callOrIndexer : expr LBRACES exprs RBRACES"""
    parameters = []
    for i, parameter in enumerate(p[3]):
        parameters.append(Parameter(exprs=parameter, index=i, pos=set_pos(p, 2), children=p[3]))
    callOrIndexer = NodeValue('callOrIndexer', children=parameters)
    expr = NodeValue('expr', children=[p[1]])
    p[0] = CallOrIndexer(expr=p[1], parameters=parameters, pos=set_pos(p, 2), children=[expr, callOrIndexer])


def p_index(p):
    """index :  identifier SQR_LBRACES expr SQR_RBRACES
    """
    name = NodeValue('ListName', children=[p[1]])
    index = NodeValue('Index', children=[p[3]])
    p[0] = Index(name=p[1], index=p[3], pos=set_pos(p, 1), children=[name, index])


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
    type = NodeValue(role='type', children=[NodeValue(role=p[1][0])])
    value = NodeValue(role='value', children=[NodeValue(role=p[1][1])])
    literal = NodeValue(role='literal', children=[type, value])
    p[0] = Literal(value=p[1][0], type=p[1][1], pos=set_pos(p, 1), children=[literal])


def p_str(p):
    """str : STR"""
    p[0] = p[1].replace('"', ''), p.slice[0].type


def p_char(p):
    """char : CHAR"""
    p[0] = p[1].replace('\'', ''), p.slice[0].type


def p_hex(p):
    """hex : HEX"""
    p[0] = p[1], p.slice[0].type


def p_bits(p):
    """bits : BITS"""
    p[0] = p[1], p.slice[0].type


def p_dec(p):
    """dec : DEC"""
    p[0] = p[1], p.slice[0].type


def p_bool(p):
    """bool : BOOL"""
    p[0] = p[1], p.slice[0].type


def p_error(p):
    print('Unexpected token:', p)


parser = yacc.yacc(debug=True)


def parse_tokens(path):
    with open(path) as file_handler:
        input_file = file_handler.read()
        root = parser.parse(input_file)
        root.set_source_name(path)
    return root
