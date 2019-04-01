import getopt
import operator
import sys
import os
import ctypes
from copy import deepcopy


class Registry:
    def __init__(self):
        self.temp_var_id = 0
        self.registry = {'#out': None,

                         '#i1': None,
                         '#i2': None,
                         '#i3': None,
                         '#i4': None,
                         '#i5': None,

                         '#s1': None,
                         '#s2': None,
                         '#s3': None,
                         '#s4': None,
                         '#s5': None,

                         '#b1': None,
                         '#b2': None,
                         '#b3': None,
                         '#b4': None,
                         '#b5': None}


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

# bin_ops_int = {'ADD': operator.add,
#                'MINUS': operator.sub,
#                'DIVIDE': operator.truediv,
#                'MUL': operator.mul,
#                'LESSEQ': operator.le,
#                'LESS': operator.lt,
#                'MOREEQ': operator.ge,
#                'MORE': operator.gt,
#                'NOTEQ': operator.ne,
#                'EQ': operator.eq}
#
# bin_ops_str = {'LESSEQ': operator.le,
#                'LESS': operator.lt,
#                'MOREEQ': operator.ge,
#                'MORE': operator.gt,
#                'ADD': operator.concat,
#                'NOTEQ': operator.ne,
#                'EQ': operator.eq}
#
# bin_ops_bool = {'AND': operator.and_,
#                 'OR': operator.or_,
#                 'LESSEQ': operator.le,
#                 'LESS': operator.lt,
#                 'MOREEQ': operator.ge,
#                 'MORE': operator.gt,
#                 'CONCAT': operator.concat,
#                 'NOTEQ': operator.ne,
#                 'EQ': operator.eq}

un_ops = {'UMINUS': operator.neg, 'NOT': operator.not_}
un_ops_int = {'UMINUS': operator.neg}
un_ops_bool = {'NOT': operator.not_}

type_mapper = {'DEC': int,
               'HEX': int,
               'BITS': int,
               'INT': int,
               'UINT': int,
               'LONG': int,
               'ULONG': int,
               'STRING': str,
               'CHAR': str,
               'BOOL': bool,
               'VOID': int}

type_to_c_types = {'DEC': ctypes.c_int,
                   'HEX': ctypes.c_int,
                   'BITS': ctypes.c_int,
                   'INT': ctypes.c_int,
                   'UINT': ctypes.c_uint,
                   'LONG': ctypes.c_long,
                   'ULONG': ctypes.c_ulong,
                   'STRING': ctypes.c_wchar_p,
                   'CHAR': ctypes.c_char,
                   'BOOL': ctypes.c_bool}

integer = {'DEC': 10,
           'HEX': 16,
           'BITS': 2,
           'INT': 10,
           'UINT': 10,
           'LONG': 10,
           'ULONG': 10}

reversed_func = ['return', 'print']

string = ['string', 'CHAR']
boolean = ['BOOL']
_type = {str(str): 'string',
         str(bool): 'bool',
         str(int): 'int'}


class Interpreter:
    # def call_rezerved(self, func, param):
    #     if func == 'return':
    #         self.return_func(param)
    #     if func == 'print':
    #         self.print_func(param)

    def __init__(self, path):
        with open(path, 'rb') as f:
            self.commands = f.read().decode().split('\n')
        self.index = 1
        self.registry = Registry()
        self.context = {'variable': {},
                        'array': {},
                        'func': {},
                        'external_func': {},
                        'class': {},
                        'stack_trace': []}
        self.parse_context()
        self.index = self.find_func('main', None)
        self.stack = []

    def parse_context(self):
        end_context = self.commands.index('ENDCONTEXT')
        while self.current()[0] not in ['ENDCONTEXT', '']:
            if self.current()[0] == 'FUNC':
                name = self.current()[1]
                param = self.current()[2] if self.current()[2] else ''
                start_line = int(self.current()[3])
                if not self.context['func'].get(self.current()[0]):
                    self.context['func'][name] = [None, {}]
                self.context['func'][name][0] = name
                # different function by parameters count and types
                self.context['func'][name][1][param] = start_line + end_context + 1
                self.next()
            if self.current()[0] == 'EXFUNC':
                lib_name = self.current()[1]
                func_name = self.current()[2]
                alias_name = self.current()[3]
                return_type = type_to_c_types[self.current()[4]]
                args = []
                for arg in self.current()[5:]:
                    args.append(type_to_c_types[arg])
                dll = ctypes.WinDLL(lib_name + '.dll')
                external_func = ctypes.WINFUNCTYPE(return_type, *args)((func_name, dll))
                self.context['external_func'][alias_name] = external_func
                self.next()

    def return_func(self, param):
        self.stack.append(*param)

    def print_func(self, param):
        print(*param)

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

    def check_context(self, name, context=None):
        context = context if context else self.context
        if not context.get(name):
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
        return self.context['func'][name][1][_args]

    def start_execute(self, context=None):
        if context:
            context = context
        else:
            context = {'variable': deepcopy(self.context['variable']),
                       'array': deepcopy(self.context['array']),
                       'func': deepcopy(self.context['func'])}
        self.base_executor(context=context)

    def base_executor(self, context=None):
        if context:
            context = context
        else:
            context = {'variable': deepcopy(self.context['variable']),
                       'array': deepcopy(self.context['array']),
                       'func': deepcopy(self.context['func'])}

        # print(context)
        while self.current()[0] not in ['EFUNC', 'ENDBLOCK', 'ENDLOOP', '']:
            # print(str(self))
            # print(str(self) + '\t\t\t\t\t\t\t' + str(context['variable']))
            # print(self.stack)
            # print(context)
            if self.current()[0] == 'EXPR':
                self.expr_executor(context=context)
                self.next()
                continue

            if self.current()[0] == 'DIM':
                self.dim_executer(context=context)
                self.next()
                continue

            if self.current()[0] == 'ASSIGN':
                assigment = self.next()
                if assigment[0] == 'VAR':
                    name = assigment[2]
                    variable = context['variable'][name]

                    self.check_context(name, context['variable'])
                    self.next()
                    self.expr_executor(context=context)
                    value = self.registry.registry['#out']

                    context['variable'][name] = (value, variable[1])
                    # print(context)
                else:
                    self.expr_executor(context=context)
                    index = self.stack.pop()
                    elem = self.stack.pop()
                    self.next()
                    self.expr_executor(context=context)
                    value = self.registry.registry['#out']

                    context['variable'][elem][0][int(index)] = value
                    print(context)

                self.next()
                continue

            if self.current()[0] == 'IF':
                self.next()
                self.expr_executor(context=context)
                if self.registry.registry['#out']:
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
                self.context['stack_trace'].append(self.current()[1])
                self.next()
                continue

            print('Unexpected command %s' % self.current())
            exit(5)
        self.context['stack_trace'].pop()
        return context
        # print(self.context)

    def expr_executor(self, context):
        expr_stack = []
        while self.current():
            # print('\t' + str(self) + '\t' + str(self.registry.registry))
            # print('\t' + str(self))
            # print('\t' + str(self.registry.registry))
            if self.current()[0] in bin_ops.keys():
                left = self.current()[1]
                right = self.current()[2]
                result = self.current()[3]

                left = self.registry.registry[left] if left in self.registry.registry.keys() else \
                context['variable'][left][0]
                right = self.registry.registry[right] if right in self.registry.registry.keys() else \
                context['variable'][right][0]

                if result in self.registry.registry.keys():
                    self.registry.registry[result] = bin_ops[self.current()[0]](left, right)
                else:
                    context['variable'][result][0] = bin_ops[self.current()[0]](left, right)

                self.next()
                continue

            if self.current()[0] in un_ops.keys():
                left = self.current()[1]
                result = self.current()[2]
                self.registry.registry[result] = un_ops[self.current()[0]](self.registry.registry[left])
                self.next()
                continue

            if self.current()[0] == 'LOAD':
                reg = self.current()[1]
                value = None
                # if type(self.registry.registry[reg]) == tuple:
                #     value = self.registry.registry[reg]
                #     value = context['array'][value[0]][0][value[1]]
                #     self.registry.registry[reg] = value
                #     self.next()
                #     continue
                if reg[1] == 'i':
                    value = int(self.current()[2])
                if reg[1] == 's':
                    value = ' '.join(self.current()[2:]).strip('\'')
                if reg[1] == 'b':
                    value = True if self.current()[2].lower() == 'true' else False
                if reg[:5] == '#TEMP':
                    context['variable'][reg] = self.current()[2]
                    self.next()
                    continue

                self.registry.registry[reg] = value
                self.next()
                continue

            if self.current()[0] == 'VARIABLE_LOAD':
                reg = self.current()[1]
                name = self.current()[2]
                value = context['variable'][name][0]
                self.registry.registry[reg] = value
                self.next()
                continue

            if self.current()[0] == 'TEMPORARY_LOAD':
                name = self.current()[1]
                context['variable'][name] = [None, None]
                self.next()
                continue

            if self.current()[0] == 'REMOVE':
                temp = self.current()[1]
                del context['variable'][temp]
                self.next()
                continue

                # if self.current()[0] == 'INDEX':
                #     name = self.next()[1]
                #     print(self.current())
                # self.expr_executor(context=context)
                # index = int(self.stack.pop())
                # value = context['variable'][name][0][index - 1][0]
                # expr_stack.append([value])
                # self.next()
                # continue

            if self.current()[0] == 'CALL':
                current_index = self.index
                self.next()
                # get name
                name = ''
                while self.current()[0] != 'ENDNAME':
                    name = self.registry.registry[self.expr_executor(context)]
                    self.next()
                    # print(name)
                self.next()
                params = []
                while self.current()[0] != 'ENDPARAMS':
                    params.append(self.registry.registry[self.expr_executor(context)])
                    self.next()
                self.next()

                if self.context['external_func'].get(name):
                    response = self.context['external_func'][name](*params)
                    self.registry.registry['#out'] = response
                    continue
                if self.context['func'].get(name):
                    params = list(reversed(params)) or ''
                    # safe registry
                    current_reg = deepcopy(self.registry.registry)
                    # safe index
                    current_index = deepcopy(self.index)

                    # execute function
                    self.index = self.context['func'][name][1]['']
                    if params:
                        self.stack += params
                    response = self.base_executor(context)

                    # return index
                    self.index = current_index

                    # return registry
                    self.registry.registry = current_reg

                    self.registry.registry['#out'] = response
                    continue

                if context['variable'].get(name):
                    self.stack.append(name)
                    self.stack.append(params[0])
                    self.registry.registry['#out'] = context['variable'].get(name)[0][params[0]]
                    continue

                print('Unknown name to call %s' % name)
                exit(5)
                # out = self.current()[1]
                # get params
                # if self.current()[2][:5] == '#TEMP':
                #     name = context[self.current()[2]][0]
                # else:
                #     name = self.registry.registry[self.current()[2]]
                # params = self.current()[3:]
                #
                # if context[name][1] == 'function':
                #     self.index = self.find_func(name, params)
                #     func_context = deepcopy(self.context)
                #     self.start_execute(func_context)
                #     # expr_stack.append(self.stack.pop())
                #     self.index = current_index
                #     self.context['stack_trace'].pop()
                #     self.next()
                #
                # if type(context[name][0]) == list:
                #     if len(params) != 1:
                #         print('Array is %s-dimensional not %s' % (1, len(params)))
                #         exit(5)
                #     self.registry.registry[out] = name, self.registry.registry[params[0]]
                #     self.next()
                continue

            if self.current()[0] == 'POP':
                self.registry.registry['#out'] = self.stack.pop()
                self.next()
                continue

            if self.current()[0] == 'EXPR':
                self.next()
                continue

            if self.current()[0] == 'ENDEXPR':
                out_req = self.current()[1]
                req = self.current()[2]
                self.registry.registry[out_req] = self.registry.registry[req]
                # print('\t\t' + str(self.registry.registry[out_req]))
                return out_req

            print('Unexpected expr command %s' % self.current())
            exit(5)
        return context

    def dim_executer(self, context):
        dim_stack = []
        name = ''
        while self.next():
            # name = self.current()[1]
            # context['variable'][name] = [None]
            # return
            if self.current()[0] == 'VAR':
                type = self.current()[1]
                name = self.current()[2]
                if type == 'ARRAY':
                    self.next()
                    while self.current()[0].upper() not in [*integer, *boolean, *string]:
                        len = int(self.current()[0])
                        context['variable'][name] = [[None for _ in range(len)], None]
                        self.next()
                    array_type = self.current()[0]
                    context['variable'][name][1] = array_type
                else:
                    context['variable'][name] = [None, type_mapper[type]]
                # print(context)
                return

    def get_index(self, _len, pos, max):
        index = 0
        for line, length in zip(pos, max):
            index += int(_len / length) * (line - 1)
