import unittest

from syntax_tree_parser import build_tree


class TetsParser(unittest.TestCase):
    def parser_test(self, code, expected):
        actual = build_tree(code)
        self.assertEqual(actual, expected)

    def test_func(self):
        input = '''
        function func_name ()
        end function
        '''

        expected = '''
        '''
        self.parser_test(input, expected)


if __name__ == '__main__':
    unittest.main()
