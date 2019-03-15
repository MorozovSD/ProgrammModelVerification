import getopt
import operator
import sys
import os
import ctypes
from copy import deepcopy

bin_ops = {'ADD': operator.add,
           'MINUS': operator.sub,
           'DIVIDE': operator.truediv,
           'MUL': operator.mul,
           'AND': operator.and_,
           'OR': operator.or_,
           'LESSEQ': operator.le,
           'LESS': operator.lt,
           'MOREEQ': operator.ge,
           'MORE': operator.gt,
           'NOTEQ': operator.ne,
           'EQ': operator.eq}

bin_ops_int = {'ADD': operator.add,
               'MINUS': operator.sub,
               'DIVIDE': operator.truediv,
               'MUL': operator.mul,
               'LESSEQ': operator.le,
               'LESS': operator.lt,
               'MOREEQ': operator.ge,
               'MORE': operator.gt,
               'NOTEQ': operator.ne,
               'EQ': operator.eq}

bin_ops_str = {'LESSEQ': operator.le,
               'LESS': operator.lt,
               'MOREEQ': operator.ge,
               'MORE': operator.gt,
               'ADD': operator.concat,
               'NOTEQ': operator.ne,
               'EQ': operator.eq}

bin_ops_bool = {'AND': operator.and_,
                'OR': operator.or_,
                'LESSEQ': operator.le,
                'LESS': operator.lt,
                'MOREEQ': operator.ge,
                'MORE': operator.gt,
                'CONCAT': operator.concat,
                'NOTEQ': operator.ne,
                'EQ': operator.eq}

un_ops = {'UMINUS': operator.neg, 'NOT': operator.not_}
un_ops_int = {'UMINUS': operator.neg}
un_ops_bool = {'NOT': operator.not_}

type_mapper = {'dec': int,
               'hex': int,
               'bits': int,
               'int': int,
               'uint': int,
               'long': int,
               'ulong': int,
               'string': str,
               'char': str,
               'bool': bool}

integer = {'DEC': 10,
           'HEX': 16,
           'BITS': 2,
           'INT': 10,
           'UINT': 10,
           'LONG': 10,
           'ULONG': 10}

reversed_func = ['return', 'print']

string = ['STR', 'CHAR']
boolean = ['BOOL']
_type = {str(str): 'str',
         str(bool): 'bool',
         str(int): 'int'}


class Interpreter:
    def call_rezerved(self, func, param):
        if func == 'return':
            self.return_func(param)
        if func == 'print':
            self.print_func(param)

    def __init__(self, path):
        with open(path, 'rb') as f:
            self.commands = f.read().decode().split('\n')
        self.index = 1
        self.context = {'variable': {},
                        'stack_trace': []}
        self.parse_context()
        print(self.context)
        self.index = self.find_func('main', None)
        self.stack = []
        print(self.commands)

    def parse_context(self):
        end_context = self.commands.index('ENDCONTEXT')
        while self.current()[0] not in ['ENDCONTEXT', '']:
            param = self.current()[1] if self.current()[1] else ''
            if not self.context['variable'].get(self.current()[0]):
                self.context['variable'][self.current()[0]] = [None, {}]
            self.context['variable'][self.current()[0]][0] = self.current()[0]
            self.context['variable'][self.current()[0]][1][param] = int(self.current()[2]) + end_context + 1
            self.next()

    def return_func(self, param):
        self.stack.append(*param)

    def print_func(self, param):
        print(*param)

    def extend_func(self, name, param):
        #     os.chdir("C:\\Program Files\\Compact Automated Testing System V2.0")
        #
        # # Load DLL into memory.
        # CATSDll = ctypes.WinDLL ("CATS.dll")
        #
        # # Set up prototype and parameters for the desired function call.
        # CATSDllApiProto = ctypes.WINFUNCTYPE (ctypes.c_uint8,ctypes.c_double)
        #
        # CATSDllApiParams = (1, "p1", 0), (1, "p2", 0),
        #
        # # Actually map the call (setDACValue) to a Python name.
        # CATSDllApi = CATSDllApiProto (("setDACValue", CATSDll), CATSDllApiParams)
        #
        # # Set up the variables and call the Python name with them.
        # p1 = ctypes.c_uint8 (1)
        # p2 = ctypes.c_double (4)
        #
        # CATSDllApi(p1,p2)
        pass

    def current(self):
        return self.commands[self.index].split(' ')

    def next(self):
        if self.index < len(self.commands) - 1:
            self.index += 1
            return self.commands[self.index].split(' ')
        return None

    def goto(self, index):
        self.index = index
        return self.commands[self.index].split(' ')

    def __repr__(self):
        return 'Current comand %s %s' % (self.current(), str(self.index + 1))

    def check_context(self, name, type, context=None):
        context = context if context else self.context
        if not context[type].get(name):
            print('Unknown %s name - %s' % (type, name))
            exit(7)

    def check_type(self, variable, value):
        if variable[1] != type(value):
            print('Incorrect type actual: %s expected: %s' % (type(value), variable[1]))
            exit(8)

    def find_func(self, name, args):
        _args = ''
        if args:
            for arg in filter(None, args):
                _args += _type[str(type(arg))] + '_'
            _args = _args[:-1]
        return self.context['variable'][name][1][_args]

    def start_execute(self, context=None):
        self.context['stack_trace'].append(self.current()[1])
        self.base_executor(context)

    def base_executor(self, context=None):
        context = context if context else deepcopy(self.context)
        # print(context)
        while self.current()[0] not in ['EFUNC', 'ENDBLOCK', 'ENDLOOP', '']:
            print(self)
            # print(context)
            if self.current()[0] == 'EXPR':
                self.expr_executor(context=context)
                self.next()
                continue

            # ['DIM', *id.byte_code(), *self.type.byte_code(), 'ENDDIM']
            if self.current()[0] == 'DIM':
                self.dim_executer(context=context)
                self.next()
                continue

            # ['ASSIGN', *id.byte_code(), 'EXPR', *self.expr.byte_code(), 'ENDEXPR', 'ASSIGN']
            if self.current()[0] == 'ASSIGN':

                assigment = self.next()

                if assigment[0] == 'INDEX':
                    name = self.next()[1]
                    # print(self.current())
                    self.expr_executor(context=context)
                    index = int(self.stack.pop())
                    variable = context['variable'][name][0][index - 1]
                    self.check_context(name, 'variable', context)
                    self.expr_executor(context=context)
                    value = self.stack.pop()

                    self.check_type(variable, value)
                    context['variable'][name][0][index - 1] = (value, variable[1])
                else:
                    name = assigment[1]
                    variable = context['variable'][name]

                    self.check_context(name, 'variable', context)
                    self.expr_executor(context=context)
                    value = self.stack.pop()

                    self.check_type(variable, value)
                    context['variable'][name] = (value, variable[1])

                self.next()
                continue

            if self.current()[0] == 'IF':
                self.next()
                self.expr_executor(context=context)
                if self.stack.pop():
                    self.next()
                self.next()
                continue

            if self.current()[0] == 'JUMP':
                self.goto(self.index + int(self.current()[1]))
                continue

            if self.current()[0] == 'BLOCK':
                self.next()
                self.base_executor(context=context)
                self.next()
                continue

            if self.current()[0] == 'LOOP':
                self.next()
                self.base_executor(context=context)
                self.next()
                continue

            if self.current()[0] == 'BREAK':
                self.goto(self.commands.index('ENDLOOP', self.index) + 1)
                continue

            if self.current()[0] == 'FUNC':
                context['stack_trace'].append(self.current()[1])
                self.next()
                continue

            print('Unexpected command %s' % self.current())
            exit(5)
        # print(self.context)

    def expr_executor(self, context):
        expr_stack = []
        while self.current():
            print('\t' + str(self))
            # print('\t' + str(expr_stack))
            if self.current()[0] in bin_ops.keys():
                right = expr_stack.pop()
                left = expr_stack.pop()
                if type(left) == int:
                    expr_stack.append(bin_ops_int[self.current()[0]](left, int(right)))
                    self.next()
                    continue
                if type(left) == str:
                    expr_stack.append(bin_ops_str[self.current()[0]](left, str(right)))
                    self.next()
                    continue
                if type(left) == bool:
                    expr_stack.append(bin_ops_bool[self.current()[0]](left, bool(right)))
                    self.next()
                    continue
                print('Unsupported binary operand %s for %s' % (bin_ops[self.current()[0]], type(left)))
                exit(6)

            if self.current()[0] in un_ops.keys():
                left = expr_stack.pop()
                if type(left) == int:
                    expr_stack.append(un_ops_int[self.current()[0]](left))
                    self.next()
                    continue
                if type(left) == bool:
                    expr_stack.append(un_ops_bool[self.current()[0]](left))
                    self.next()
                    continue
                print('Unsupported unary operand %s for %s' % (un_ops[self.current()[0]], type(left)))
                exit(6)

            if self.current()[0] in integer.keys():
                _type = self.current()[0]
                value = self.next()[0]
                expr_stack.append(int(value, base=integer[_type]))
                self.next()
                continue

            if self.current()[0] in string:
                value = self.next()[0]
                expr_stack.append(str(value))
                self.next()
                continue

            if self.current()[0] in boolean:
                value = self.next()[0]
                expr_stack.append(bool(value))
                self.next()
                continue

            if self.current()[0] == 'VAR':
                name = self.current()[1]
                if name in reversed_func:
                    expr_stack.append(name)
                    self.next()
                    continue
                value = context['variable'][name][0]
                if value:
                    expr_stack.append(value)
                self.next()
                continue

            if self.current()[0] == 'INDEX':
                name = self.next()[1]
                # print(self.current())
                self.expr_executor(context=context)
                index = int(self.stack.pop())
                value = context['variable'][name][0][index - 1][0]
                expr_stack.append(value)
                self.next()
                continue

            if self.current()[0] == 'CALL':
                self.next()
                self.expr_executor(context=context)
                name = str(self.stack.pop())
                params = []
                self.next()
                self.next()
                while self.current()[0] != 'ENDPARAM':
                    self.expr_executor(context=context)
                    params.append(self.stack[-1])
                    self.next()
                current_indeex = self.index
                if name in reversed_func:
                    self.call_rezerved(name, params)
                else:
                    self.index = self.find_func(name, params)
                    func_context = deepcopy(self.context)
                    self.start_execute(func_context)
                    # expr_stack.append(self.stack.pop())
                    self.index = current_indeex
                    self.context['stack_trace'].pop()
                self.next()
                continue

            if self.current()[0] == 'POP':
                expr_stack.append(self.stack.pop())
                self.next()
                continue

            if self.current()[0] == 'EXPR':
                self.next()
                continue

            if self.current()[0] == 'ENDEXPR':
                self.stack.extend(expr_stack)
                return

            print('Unexpected expr command %s' % self.current())
            exit(5)

    def dim_executer(self, context):
        dim_stack = [None]
        name = ''
        while self.next():
            if self.current()[0] == 'VAR':
                name = self.current()[1]
                continue

            if self.current()[0] == 'ARRAY':
                dim_stack.append(int(self.next()[0]))
                continue

            if self.current()[0] in type_mapper.keys():
                _type = type_mapper[self.current()[0]]
                array = dim_stack.pop()
                if array:
                    context['variable'][name] = ([[None, _type] for _ in range(array)], list)
                else:
                    context['variable'][name] = (None, _type)

                return


# def usage():
#     print("""Run example:
#     python interpreter.py -i ../output/linear_code.bin, -s test_binary
#     Arguments:
#     -i (--input)  - input files
#     -s (--start)  - starting function
#     -v            - detailed output
#     --help        - help
#     """)
#
#
# def main():
#     try:
#         opts, args = getopt.getopt(sys.argv[1:], 'vi:o:v', ['help', 'start=', 'input='])
#     except getopt.GetoptError:
#         usage()
#         sys.exit(2)
#     start_func = ''
#     input = None
#     verbose = False
#     for o, a in opts:
#         if o == '-v':
#             verbose = True
#         if o in ('-h', '--help'):
#             usage()
#             sys.exit()
#         if o in ('-s', '--start'):
#             start_func = a
#         if o in ('-i', '--input'):
#             input = a.split(',')
#     if input is None:
#         print('Input file doesn\'t set. Use -i to set input files')
#         usage()
#         sys.exit(2)
#
#     interpreter = Interpreter(input, start_func)
#     interpreter.start_execute()
#
#
# if __name__ == "__main__":
#     main()
