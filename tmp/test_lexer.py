import unittest
from tmp import lexer, tokens


class TestLexer(unittest.TestCase):
    def lexer_test(self, code, expected):
        actual = lexer.lex(code, tokens.get())
        self.assertEqual(expected, actual)

    def test_negative(self):
        self.lexer_test('@', None)

    def test_empty(self):
        self.lexer_test('', [])

    def test_id(self):
        self.lexer_test('abc', [('abc', tokens.ID)])

    def test_binary(self):
        self.lexer_test('+ - / * and or == != >= > <= <', [('+', tokens.BINARY),
                                                           ('-', tokens.BINARY),
                                                           ('/', tokens.BINARY),
                                                           ('*', tokens.BINARY),
                                                           ('and', tokens.BINARY),
                                                           ('or', tokens.BINARY),
                                                           ('==', tokens.BINARY),
                                                           ('!=', tokens.BINARY),
                                                           ('>=', tokens.BINARY),
                                                           ('>', tokens.BINARY),
                                                           ('<=', tokens.BINARY),
                                                           ('<', tokens.BINARY)])

    def test_builtin(self):
        self.lexer_test('bool byte int uint long ulong char string', [('bool', tokens.BUILTIN),
                                                                      ('byte', tokens.BUILTIN),
                                                                      ('int', tokens.BUILTIN),
                                                                      ('uint', tokens.BUILTIN),
                                                                      ('long', tokens.BUILTIN),
                                                                      ('ulong', tokens.BUILTIN),
                                                                      ('char', tokens.BUILTIN),
                                                                      ('string', tokens.BUILTIN)])

    def test_assignment(self):
        self.lexer_test('=', [('=', tokens.ASSIGNMENT)])

    def test_space(self):
        self.lexer_test(' \t\n #fdsfsdfsdf', [])

    def test_bracers(self):
        self.lexer_test('()', [('(', tokens.BRACES),
                               (')', tokens.BRACES)])

    def test_reserved(self):
        self.lexer_test('as ,functionendifthenelsewhilewenddoloopuntilbreak; ', [(r'as', tokens.RESERVED),
                                                                                 (r',', tokens.RESERVED),
                                                                                 (r'function', tokens.RESERVED),
                                                                                 (r'end', tokens.RESERVED),
                                                                                 (r'if', tokens.RESERVED),
                                                                                 (r'then', tokens.RESERVED),
                                                                                 (r'else', tokens.RESERVED),
                                                                                 (r'while', tokens.RESERVED),
                                                                                 (r'wend', tokens.RESERVED),
                                                                                 (r'do', tokens.RESERVED),
                                                                                 (r'loop', tokens.RESERVED),
                                                                                 (r'until', tokens.RESERVED),
                                                                                 (r'break', tokens.RESERVED),
                                                                                 (r';', tokens.RESERVED)])

    def test_literal(self):
        self.lexer_test('\"wegwgs23tgs632#@@#%falseas\" \'1\' 0x0654abcdfABCF 0b010101001 053252352 true false',
                        [('\"wegwgs23tgs632#@@#%falseas\"', tokens.STR),
                         ('\'1\'', tokens.CHAR),
                         (r'0x0654abcdfABCF', tokens.HEX),
                         (r'0b010101001', tokens.BITS),
                         (r'053252352', tokens.DEC),
                         (r'true', tokens.BOOL),
                         (r'false', tokens.BOOL)])

    def test_complex(self):
        self.lexer_test('x1231 + (we143 * rewq1) = fewq',
                        [('x1231', tokens.ID),
                         ('+', tokens.BINARY),
                         ('(', tokens.BRACES),
                         ('we143', tokens.ID),
                         ('*', tokens.BINARY),
                         ('rewq1', tokens.ID),
                         (')', tokens.BRACES),
                         ('=', tokens.ASSIGNMENT),
                         ('fewq', tokens.ID)])


if __name__ == '__main__':
    unittest.main()
