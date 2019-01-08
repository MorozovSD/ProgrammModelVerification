ASSIGNMENT = 'ASSIGNMENT'
BINARY = 'BINARY'
ID = 'ID'
BRACES = 'BRACES'
BUILTIN = 'BUILTIN'
RESERVED = 'RESERVED'
STR = 'STR'
CHAR = 'CHAR'
HEX = 'HEX'
BITS = 'BITS'
DEC = 'DEC'
BOOL = 'BOOL'

tokens = [
    # Комментарии и пробелы
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    # Типы данных
    (r'bool', BUILTIN),
    (r'byte', BUILTIN),
    (r'int', BUILTIN),
    (r'uint', BUILTIN),
    (r'long', BUILTIN),
    (r'ulong', BUILTIN),
    (r'char', BUILTIN),
    (r'string', BUILTIN),
    # Зарезервированные конструкции языка
    (r'as', RESERVED),
    (r',', RESERVED),
    (r'function', RESERVED),
    (r'end', RESERVED),
    (r'if', RESERVED),
    (r'then', RESERVED),
    (r'else', RESERVED),
    (r'while', RESERVED),
    (r'wend', RESERVED),
    (r'do', RESERVED),
    (r'loop', RESERVED),
    (r'until', RESERVED),
    (r'break', RESERVED),
    (r';', RESERVED),
    (r'until', RESERVED),
    # Бинарные операции
    (r'\+', BINARY),
    (r'\-', BINARY),
    (r'/', BINARY),
    (r'\*', BINARY),
    (r'<=', BINARY),
    (r'<', BINARY),
    (r'>=', BINARY),
    (r'>', BINARY),
    (r'!=', BINARY),
    (r'==', BINARY),
    (r'and', BINARY),
    (r'or', BINARY),
    # Присваивание
    (r'=', ASSIGNMENT),
    # Скобки
    (r'\(', BRACES),
    (r'\)', BRACES),
    # Литералы
    (r'"[^\"\\]*(?:\\.[^\"\\]*)*\"', STR),
    (r'\'[^\']\'', CHAR),
    (r'0[xX][0-9A-Fa-f]+', HEX),
    (r'0[bB][01]+', BITS),
    (r'[0-9]+', DEC),
    (r'(true)|(false)', BOOL),
    # Идентификаторы
    (r'[a-zA-Z_][a-zA-Z_0-9]*', ID),
]


def get():
    return tokens
