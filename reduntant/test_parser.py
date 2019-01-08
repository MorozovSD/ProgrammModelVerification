import unittest

from reduntant import lexer, tokens
from reduntant.combinators import *

id = Tag(tokens.ID)
string = Tag(tokens.STR)
char = Tag(tokens.CHAR)
hex_number = Tag(tokens.HEX)
bits = Tag(tokens.BITS)
dec = Tag(tokens.DEC)
boolean = Tag(tokens.BOOL)

def keyword(s):
    return Reserved(s, tokens.RESERVED)


def binary_operand(s):
    return Reserved(s, tokens.BINARY)


class TestCombinators(unittest.TestCase):
    def combinator_test(self, code, parser, expected):
        token_list = lexer.lex(code, tokens.get())
        result = parser(token_list, 0)
        self.assertNotEqual(None, result)
        self.assertEqual(expected, result.value)

    # def test_tag(self):
    #     self.combinator_test('if', Tag(tokens.RESERVED), 'if')

    # def test_reserved(self):
    #     self.combinator_test('if', Reserved('if', tokens.RESERVED), 'if')
    #
    def test_concat(self):
        self.combinator_test('x y', id + id, ('x', 'y'))

    # def test_concat_associativity(self):
    #     parser = id + id + id
    #     self.combinator_test('x y z', parser, (('x', 'y'), 'z'))
    #
    # def test_exp_sugar(self):
    #     separator = binary_operand('+') ^ (lambda x: lambda l, r: l + r)
    #     parser = id * separator
    #     self.combinator_test('x + y + z', parser, 'xyz')
    #
    # def test_alternate_sugar(self):
    #     parser = id | dec
    #     self.combinator_test('x', parser, 'x')
    #     self.combinator_test('12', parser, '12')
    #
    # def test_opt(self):
    #     parser = Opt(id)
    #     self.combinator_test('x', parser, 'x')
    #     self.combinator_test('12', parser, None)
    #
    # def test_rep(self):
    #     parser = Rep(id)
    #     self.combinator_test('', parser, [])
    #     self.combinator_test('x y z werw', parser, ['x', 'y', 'z', 'werw'])
    #
    # def test_process(self):
    #     parser = Process(dec, int)
    #     self.combinator_test('12', parser, 12)
    #
    # def test_process_sugar(self):
    #     parser = dec ^ int
    #     self.combinator_test('12', parser, 12)
    #
    # def test_lazy(self):
    #     def get_parser():
    #         return id
    #
    #     parser = Lazy(get_parser)
    #     self.combinator_test('x', parser, 'x')

    # def test_phrase(self):
    #     parser = Phrase(id)
    #     self.combinator_test('x', parser, 'x')


if __name__ == '__main__':
    unittest.main()
