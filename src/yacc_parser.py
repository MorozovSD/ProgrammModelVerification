import ply.yacc as yacc
from node import Node

from ply_lex import tokens


def find_column(data, pos):
    line_start = data.rfind('\n', 0, pos) + 1
    return (pos - line_start) + 1


def set_info(p, pos=1):
    return '(line: ' + str(p.lineno(pos)) + ' : pos: ' + str(find_column(p.lexer.lexdata, p.lexpos(pos))) + ')'


class NodeLabel:
    count = {}

    def __init__(self, name, info=''):
        if name in self.count:
            NodeLabel.count[name] += 1
        else:
            NodeLabel.count[name] = 1
        self.count = NodeLabel.count[name]
        self.name = name
        self.info = info

    def __repr__(self):
        return str(self.name) + '(' + str('id: ' + str(self.count)) + ')'


class LeafContent:

    def __init__(self, p, type=None, index=1, info='', replace=''):
        self.type = type
        self.name = p[index].replace(replace, '')
        self.pos = find_column(p.lexer.lexdata, p.lexpos(index))
        self.line = p.lineno(index)
        self.info = info

    def __repr__(self):
        return str(self.name) + str((self.line, self.pos))


def p_source(p):
    """source :
    | sourceItem"""
    p[0] = Node(NodeLabel('source'), [p[1]])


def p_sourceItem(p):
    """sourceItem :
    | funcDefs"""
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = Node(NodeLabel('sourceItem'), p[1])


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
    p[0] = Node(NodeLabel('funcDef'), [p[2], p[3]])


def p_funcSignature(p):
    """funcSignature : identifier LBRACES argDefs RBRACES AS typeRef
                     | identifier LBRACES argDefs RBRACES"""
    expr_node = []
    if p[3] is not None:
        expr_node += [*p[3]] if type(p[3]) == list else expr_node.append(p[3])
    if len(p) == 7:
        p[0] = Node(NodeLabel('funcSignature'), expr_node + [p[6]], p[1])
    else:
        p[0] = Node(NodeLabel('funcSignature'), expr_node, p[1])


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
        p[0] = Node(NodeLabel('argDef'), [p[3]], p[1])
    else:
        p[0] = Node(NodeLabel('argDef'), None, [p[1]])


def p_typeRef(p):
    """typeRef : builtin
               | custom
               | array"""
    if type(p[1]) == Node:
        p[0] = Node(NodeLabel('typeRef'), [p[1]])
    else:
        p[0] = Node(NodeLabel('typeRef'), None, p[1])


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
    p[0] = LeafContent(p, 'builtin')


def p_custom(p):
    """custom : identifier"""
    p[0] = Node(NodeLabel('custom'), leaf=p[1])


def p_array(p):
    """array : typeRef LBRACES commas RBRACES"""
    p[0] = Node(NodeLabel('array'), [p[1]])


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
        p[0] = p[1]


def p_identifier(p):
    """identifier : IDENTIFIER"""
    p[0] = LeafContent(p, 'identifier')


def p_statements(p):
    """statements : pre_statements
    """
    p[0] = Node(NodeLabel('statements'), p[1]) if p[1] is not None else None



def p_statement_nodes(p):
    """pre_statements :
                  | statement pre_statements
                  | statement
    """
    if len(p) == 1:
        p[0] = None
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
    p[0] = Node(NodeLabel('new_variable', set_info(p)), [p[4]], p[2])


def p_if(p):
    """if : IF expr THEN statements END IF
          | IF expr THEN statements ELSE statements END IF"""
    expr_node = []
    expr_leaf = []
    expr_node.append(p[2]) if type(p[2]) == Node else expr_leaf.append(p[2])
    if len(p) == 7:
        expr_node.append(p[4])
        p[0] = Node(NodeLabel('if'), expr_node, expr_leaf)
    else:
        expr_node += [p[4], p[6]]
        p[0] = Node(NodeLabel('if_else'), expr_node, expr_leaf)


def p_while(p):
    """while : WHILE expr statements WEND"""
    expr_node = [p[3]]
    expr_leaf = []
    expr_node.append(p[2]) if type(p[2]) == Node else expr_leaf.append(p[2])
    p[0] = Node(NodeLabel('while'), expr_node, expr_leaf)


def p_do(p):
    """do : DO statements LOOP WHILE expr
          | DO statements LOOP UNTIL expr"""
    expr_node = [p[2]]
    expr_leaf = []
    expr_node.append(p[5]) if type(p[5]) == Node else expr_leaf.append(p[5])
    p[0] = Node(NodeLabel('do ' + p[4]), expr_node, expr_leaf)


def p_break(p):
    """break : BREAK"""
    p[0] = Node(NodeLabel('break', set_info(p)), [])


def p_expression(p):
    """expression : expr SEMICOLON"""
    p[0] = p[1]


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
    expr_node = []
    expr_leaf = []
    expr_node.append(p[1]) if type(p[1]) == Node else expr_leaf.append(p[1])
    expr_node.append(p[3]) if type(p[3]) == Node else expr_leaf.append(p[3])

    node = Node(NodeLabel(p[2]), expr_node, expr_leaf)
    p[0] = Node(NodeLabel('Binary ', set_info(p, pos=2)), [node])


def p_unary(p):
    """unary : NOT expr
             | MINUS expr
    """
    expr_node = []
    expr_leaf = []
    expr_node.append(p[2]) if type(p[2]) == Node else expr_leaf.append(p[2])
    node = Node(NodeLabel(p[1]), expr_node, expr_leaf)
    p[0] = Node(NodeLabel('unary'), [node])


def p_assignment(p):
    """assignment : identifiers ASSIGNMENT expr
    """
    expr_node = []
    expr_leaf = []
    expr_node.append(p[3]) if type(p[3]) == Node else expr_leaf.append(p[3])

    if type(p[1]) == list:
        expr_leaf += [*p[1]]
        p[0] = Node(NodeLabel('assign'), expr_node, expr_leaf)
    else:
        expr_leaf.append(p[1])
        p[0] = Node(NodeLabel('assign'), expr_node, expr_leaf)


def p_braces(p):
    """braces : LBRACES expr RBRACES"""
    expr_node = []
    expr_leaf = []
    expr_node.append(p[2]) if type(p[2]) == Node else expr_leaf.append(p[2])
    p[0] = Node(NodeLabel('Brace'), expr_node, expr_leaf)


def p_callOrIndexer(p):
    """callOrIndexer : expr LBRACES exprs RBRACES"""
    expr_node = []
    expr_leaf = []
    expr_node.append(p[1]) if type(p[1]) == Node else expr_leaf.append(p[1])
    # expr_node += [*p[3]] if type(p[3]) == list else expr_node.append(p[3])
    if type(p[3]) == list:
        for expr in p[3]:
            expr_node.append(expr) if type(expr) == Node else expr_leaf.append(expr)
    else:
        expr_node.append(p[3]) if type(p[3]) == Node else expr_leaf.append(p[3])

    p[0] = Node(NodeLabel('callOrIndexer'), expr_node, expr_leaf)


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
    p[0] = Node(NodeLabel('literal'), [p[1]])


def p_str(p):
    """str : STR"""
    p[0] = Node(NodeLabel('str'), leaf=[LeafContent(p, 'hex', replace='"')])


def p_char(p):
    """char : CHAR"""
    p[0] = Node(NodeLabel('char'), leaf=[LeafContent(p, 'hex', replace='\'')])


def p_hex(p):
    """hex : HEX"""
    p[0] = Node(NodeLabel('hex'), leaf=[LeafContent(p, 'hex')])


def p_bits(p):
    """bits : BITS"""
    p[0] = Node(NodeLabel('bits'), leaf=[LeafContent(p, 'bits')])


def p_dec(p):
    """dec : DEC"""
    p[0] = Node(NodeLabel('dec'), leaf=[LeafContent(p, 'dec')])


def p_bool(p):
    """bool : BOOL"""
    p[0] = Node(NodeLabel('bool'), leaf=[LeafContent(p, 'bool')])


def p_error(p):
    print('Unexpected token:', p)


parser = yacc.yacc(debug=True)


def parse_tokens(code):
    return parser.parse(code)
