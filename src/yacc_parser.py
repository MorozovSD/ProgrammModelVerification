import ply.yacc as yacc
from node import Node
from anytree import Node as NewNode, RenderTree
# import tree_creator
from ply_lex import tokens


def find_column(input, pos):
    line_start = input.rfind('\n', 0, pos) + 1
    return (pos - line_start) + 1


def node_content(p, pos=1):
    return p[pos], p.lineno(pos), find_column(p.lexer.lexdata, p.lexpos(pos))


def p_source(p):
    """source :
    | sourceItem"""
    p[0] = Node('source', [p[1]])


def p_sourceItem(p):
    """sourceItem :
    | funcDefs"""
    p[0] = Node('sourceItem', [p[1]])


def p_funcDefs(p):
    """funcDefs : funcDef funcDefs
        | funcDef"""
    if len(p) == 3:
        p[0] = p[1].add_parts([p[2]])
    else:
        p[0] = p[1]


def p_funcDef(p):
    """funcDef : FUNCTION funcSignature statements END FUNCTION"""
    p[0] = Node('funcDef', [p[2], p[3]])


def p_funcSignature(p):
    """funcSignature : identifier LBRACES argDefs RBRACES AS typeRef
                     | identifier LBRACES argDefs RBRACES"""
    if len(p) == 7:
        p[0] = Node('funcSignature', [p[1], p[3], p[6]])
    else:
        p[0] = Node('funcSignature', [p[1], p[3]])


def p_argDefs(p):
    """argDefs :
               | argDefs COMMA
               | argDef"""
    if len(p) == 3:
        p[0] = p[1].add_parts([p[2]])
    if len(p) == 2:
        p[0] = p[1]


def p_argDef(p):
    """argDef : identifier
              | identifier AS typeRef"""
    if len(p) == 4:
        p[0] = Node('argDef', [p[1], p[3]])
    else:
        p[0] = Node('argDef', [p[1]])


def p_typeRef(p):
    """typeRef : builtin
               | custom
               | array"""
    p[0] = Node('typeRef', [p[1]])


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
    p[0] = Node('builtin', [node_content(p)])


def p_custom(p):
    """custom : identifier"""
    p[0] = Node('custom', [p[1]])


def p_array(p):
    """array : typeRef LBRACES commas RBRACES"""
    p[0] = Node('array', [p[1]])


def p_commas(p):
    """commas : commas COMMA
              | COMMA"""


def p_identifiers(p):
    """identifiers : identifiers COMMA identifier
                   | identifier"""
    if len(p) == 4:
        p[0] = p[1].add_parts([p[2]])
    else:
        p[0] = p[1]


def p_identifier(p):
    """identifier : IDENTIFIER"""
    p[0] = Node('identifier', [node_content(p)])


def p_statements(p):
    """statements :
                  | statements statement
                  | statement
    """
    if len(p) == 3:
        p[0] = p[1].add_parts([p[2]])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None


def p_statement(p):
    """statement : var
                 | assignment
                 | if
                 | while
                 | do
                 | break
                 | expression"""
    p[0] = p[1]


def p_var(p):
    """var : DIM identifiers AS typeRef"""
    p[0] = Node('new_variable', [p[2], p[4]])


def p_if(p):
    """if : IF expr THEN statements END IF
          | IF expr THEN statements ELSE statements END IF"""
    if len(p) == 7:
        p[0] = Node('if', [p[2], p[4]])
    else:
        p[0] = Node('if_else', [p[2], p[4], p[6]])


def p_while(p):
    """while : WHILE expr statements WEND"""
    p[0] = Node('while', [p[2], p[3]])


def p_do(p):
    """do : DO statements LOOP WHILE expr
          | DO statements LOOP UNTIL expr"""
    p[0] = Node('do ' + p[4], [p[2], p[5]])


def p_break(p):
    """break : BREAK"""
    p[0] = Node('break', [])


def p_expression(p):
    """expression : expr SEMICOLON"""
    p[0] = p[1]


def p_exprs(p):
    """exprs : exprs COMMA
             | expr
    """
    if len(p) == 2:
        p[0] = Node('expr', [p[1]])
    else:
        p[0] = p[1]


def p_expr(p):
    """expr : binary
            | unary
            | braces
            | callOrIndexer
            | place
            | literal
    """
    p[0] = Node('expr', [p[1]])


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
    p[0] = Node('Binary ' + p[3] + ':', [p[2], p[4]])


def p_unary(p):
    """unary : NOT expr
             | MINUS expr
    """
    p[0] = Node('unary ' + p[1], [p[2]])


def p_assignment(p):
    """assignment : identifiers ASSIGNMENT expr
    """
    p[0] = Node('assign', [p[1], p[3]])


def p_braces(p):
    """braces : LBRACES expr RBRACES"""
    p[0] = Node('Brace', [p[2]])


def p_callOrIndexer(p):
    """callOrIndexer : expr LBRACES exprs RBRACES"""
    p[0] = Node('callOrIndexer', [p[1]])


def p_place(p):
    """place : identifier"""
    p[0] = Node('variable', [p[1]])


def p_literal(p):
    """literal : bool
               | str
               | char
               | hex
               | bits
               | dec"""
    p[0] = Node('literal', [p[1]])


def p_str(p):
    """str : STR"""
    p[0] = Node('str', [node_content(p)])


def p_char(p):
    """char : CHAR"""
    p[0] = Node('char', [node_content(p)])


def p_hex(p):
    """hex : HEX"""
    p[0] = Node('hex', [node_content(p)])


def p_bits(p):
    """bits : BITS"""
    p[0] = Node('bits', [node_content(p)])


def p_dec(p):
    """dec : DEC"""
    p[0] = Node('dec', [node_content(p)])


def p_bool(p):
    """bool : BOOL"""
    p[0] = Node('bool', [node_content(p)])


def p_error(p):
    print('Unexpected token:', p)


parser = yacc.yacc(debug=True)


def build_tree(code):
    return parser.parse(code)
