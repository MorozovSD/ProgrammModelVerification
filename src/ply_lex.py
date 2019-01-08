import ply.lex as lex
from ply.lex import TOKEN
import re

tokens = (
    # Типы переменных
    'BUILTIN_BOOL',
    'BUILTIN_BYTE',
    'BUILTIN_INT',
    'BUILTIN_UINT',
    'BUILTIN_LONG',
    'BUILTIN_ULONG',
    'BUILTIN_CHAR',
    'BUILTIN_STRING',
    'BUILTIN_LIST',
    # Зарезервированные конструкции языка
    'AS',
    'FUNCTION',
    'END',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'WEND',
    'DO',
    'LOOP',
    'UNTIL',
    'BREAK',
    'COMMA',
    'COLON',
    'SEMICOLON',
    'DIM',
    # Операции
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MUL',
    'LESS_EQ',
    'LESS',
    'MORE_EQ',
    'MORE',
    'NOT_EQ',
    'EQUAL',
    'AND',
    'OR',
    'NOT',
    'ASSIGNMENT',
    'LBRACES',
    'RBRACES',
    # Переменные
    'BOOL',
    'BYTE',
    'DEC',
    'HEX',
    'BITS',
    'INT',
    'UINT',
    'LONG',
    'ULONG',
    'CHAR',
    'STR',
    # Имена переменных
    'IDENTIFIER',
    'ILLEGAL_TYPE'
)
reserved = {
    'bool': 'BUILTIN_BOOL',
    'byte': 'BUILTIN_BYTE',
    'int': 'BUILTIN_INT',
    'uint': 'BUILTIN_UINT',
    'long': 'BUILTIN_LONG',
    'ulong': 'BUILTIN_ULONG',
    'char': 'BUILTIN_CHAR',
    'string': 'BUILTIN_STRING',
    'list': 'LIST',
    'as': 'AS',
    'function': 'FUNCTION',
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'wend': 'WEND',
    'do': 'DO',
    'loop': 'LOOP',
    'until': 'UNTIL',
    'break': 'BREAK',
    'dim': 'DIM',
    'true': 'BOOL',
    'false': 'BOOL',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}
ident = r'[a-zA-Z_][a-zA-Z_0-9]*'
dec = r'[0-9]+([xXbB][0-9A-Fa-f]+)?'

t_COMMA = r','
t_COLON = r';'
t_SEMICOLON = r':'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = '/'
t_MUL = r'\*'
t_LESS_EQ = r'<='
t_LESS = r'<'
t_MORE_EQ = r'>='
t_MORE = r'>'
t_NOT_EQ = r'!='
t_EQUAL = r'=='

t_ASSIGNMENT = r'='

t_LBRACES = r'\('
t_RBRACES = r'\)'

t_STR = r'"[^\"\\]*(?:\\.[^\"\\]*)*\"'
t_CHAR = r'\'[^\']\''


@TOKEN(dec)
def t_DEC(t):
    regex_dec = re.compile(r'^[0-9]+$')
    regex_bits = re.compile(r'^0[bB][01]+$')
    regex_hex = re.compile(r'^0[xX][0-9A-Fa-f]+$')
    if regex_bits.match(t.value.lower()):
        t.type = 'BITS'
    elif regex_hex.match(t.value.lower()):
        t.type = 'HEX'
    elif regex_dec.match(t.value.lower()):
        t.type = 'DEC'
    else:
        t.type = 'ILLEGAL_TYPE'
    return t


@TOKEN(ident)
def t_IDENTIFIER(t):
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_comment(t):
    r"""#[^\n]*"""
    pass


# здесь мы игнорируем незначащие символы. Нам ведь все равно, написано $var=$value или $var   =  $value
t_ignore = ' \r\t\f'


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)
    # t.lexer.lexpos = 0


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# а здесь мы обрабатываем ошибки. Кстати заметьте формат названия функции
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.type = 'ILLEGAL_TYPE'


lexer = lex.lex(reflags=re.DOTALL)


if __name__ == "__main__":
    with open('test_input.txt') as file_handler:
        input_data = file_handler.read()

    lexer.input(input_data)

    while True:
        tok = lexer.token()  # читаем следующий токен
        if not tok:
            break  # закончились печеньки
        tok.lexpos = find_column(input_data, tok)
        print(tok)
