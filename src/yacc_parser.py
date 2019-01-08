import ply.yacc as yacc
from node import Node
from ply_lex import tokens


def p_source(p):
    """source : sourceItem"""
    print(len(p))
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = p[1]


def p_sourceItem(p):
    """sourceItem : funcDef"""


def p_funcDef(p):
    """funcDef : FUNCTION funcSignature statements END FUNCTION"""


def p_funcSignature(p):
    """funcSignature : identifier LBRACES argDefs RBRACES AS typeRef"""


def p_argDefs(p):
    """argDefs :
    | argDefs COMMA
    | argDef"""


def p_argDef(p):
    """argDef :
    | identifier
    | identifier AS typeRef"""


def p_typeRef(p):
    """typeRef :
    | builtin
    | custom
    | array"""


def p_builtin(p):
    """builtin :
    | BUILTIN_BOOL
    | BUILTIN_BYTE
    | BUILTIN_INT
    | BUILTIN_UINT
    | BUILTIN_LONG
    | BUILTIN_ULONG
    | BUILTIN_CHAR
    | BUILTIN_STRING
    | BUILTIN_LIST"""


def p_custom(p):
    """custom : identifier"""


def p_array(p):
    """array :
     | typeRef LBRACES commas RBRACES"""


def p_commas(p):
    """commas :
    | commas COMMA
    | COMMA"""


def p_identifiers(p):
    """identifiers :
    | identifiers COMMA
    | identifier"""


def p_identifier(p):
    """identifier : IDENTIFIER"""


def p_statements(p):
    """statements :
            | statements statement
            | statement
    """


def p_statement(p):
    """statement :
            | var
            | if
            | while
            | do
            | break
            | expression"""


def p_var(p):
    """var : DIM identifiers AS typeRef"""


def p_if(p):
    """if :
    | IF expr THEN statements END IF
    | IF expr THEN statements ELSE statements END IF"""


def p_while(p):
    """while : WHILE expr statements WEND"""


def p_do(p):
    """do :
    | DO statements LOOP WHILE expr
    | DO statements LOOP UNTIL expr"""


def p_break(p):
    """break : BREAK"""


def p_expression(p):
    """expression : expr SEMICOLON"""


def p_exprs(p):
    """exprs :
            | exprs COMMA
            | expr
    """


def p_expr(p):
    """expr :
            | binary
            | unary
            | braces
            | callOrIndexer
            | place
            | literal
    """


def p_binary(p):
    """binary :
            | expr PLUS expr
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
    # p[0] = Node('Binary ' + p[3] + ':', [p[2], p[4]])


def p_unary(p):
    """unary :
            | NOT expr
            | MINUS expr
    """


def p_braces(p):
    """braces : LBRACES expr RBRACES"""


def p_callOrIndexer(p):
    """callOrIndexer : expr LBRACES exprs RBRACES"""


def p_place(p):
    """place : identifier"""


def p_literal(p):
    """literal :
    | bool
    | str
    | char
    | hex
    | bits
    | dec"""


def p_str(p):
    """str : STR"""
    p[0] = Node('str', [p[1]])


def p_char(p):
    """char : CHAR"""
    p[0] = Node('str', [p[1]])


def p_hex(p):
    """hex : HEX"""
    p[0] = Node('hex', [p[1]])


def p_bits(p):
    """bits : BITS"""
    p[0] = Node('bits', [p[1]])


def p_dec(p):
    """dec : DEC"""
    p[0] = Node('dec', [p[1]])


def p_bool(p):
    """bool : BOOL"""
    p[0] = Node('bool', [p[1]])


def p_error(p):
    print('Unexpected token:', p)


parser = yacc.yacc()


def build_tree(code):
    return parser.parse(code)
