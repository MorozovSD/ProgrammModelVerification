import getopt
import operator
import sys
import os
import ctypes
from copy import deepcopy

WARNING = '\033[93m'
ENDC = '\033[0m'


class req:
    def __init__(self, state, value):
        self.state = state
        self.value = value

    def free(self):
        self.state = 'free'

    def busy(self):
        self.state = 'busy'


class registry:
    def __init__(self):
        self.temp_var_id = 0
        self.out_reg = req('free', '#out')
        self.registry_int = [req('free', '#i1'),
                             req('free', '#i2'),
                             req('free', '#i3')]

        self.registry_str = [req('free', '#s1'),
                             req('free', '#s2'),
                             req('free', '#s3')]

        self.registry_bool = [req('free', '#b1'),
                              req('free', '#b2'),
                              req('free', '#b3')]

    def free(self, value):
        for reg in self.registry_int:
            if reg.value == value:
                reg.free()
                return

        for reg in self.registry_str:
            if reg.value == value:
                reg.free()
                return

        for reg in self.registry_bool:
            if reg.value == value:
                reg.free()
                return

    def free_all(self):
        for reg in self.registry_int:
            reg.free()

        for reg in self.registry_str:
            reg.free()

        for reg in self.registry_bool:
            reg.free()

    def find_free(self, type):
        if type in integer:
            for reg in self.registry_int:
                if reg.state == 'free':
                    reg.state = 'busy'
                    return reg.value
            print(WARNING + 'No free integer registry, create temp variable' + ENDC)
        if type in string:
            for reg in self.registry_str:
                if reg.state == 'free':
                    reg.state = 'busy'
                    return reg.value
            print(WARNING + 'No free string registry, create temp variable' + ENDC)
        if type in boolean:
            for reg in self.registry_bool:
                if reg.state == 'free':
                    reg.state = 'busy'
                    return reg.value
            print(WARNING + 'No free boolean registry, create temp variable' + ENDC)
        self.temp_var_id += 1
        return '#TEMP_' + str(self.temp_var_id)


bin_ops = ['ADD', 'MINUS', 'DIVIDE', 'MUL', 'AND', 'OR', 'LESSEQ', 'LESS', 'MOREEQ', 'MORE', 'NOTEQ', 'EQ']
un_ops = ['UMINUS', 'NOT']

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

string = ['string', 'CHAR']
boolean = ['BOOL']
_type = {str(str): 'string',
         str(bool): 'bool',
         str(int): 'int'}


class ExprCoder:
    def __init__(self, expr):
        self.commands = expr
        self.index = 0
        self.stack = []
        self.registry_command = []
        self.registry = registry()

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

    def expr_executor(self):
        expr_stack = []
        while self.current():
            if self.current()[0] in bin_ops:
                right = expr_stack.pop()
                left = expr_stack.pop()
                self.registry_command.append(self.current()[0] + ' ' + left + ' ' + right)
                if right[:2] == '#T':
                    self.registry_command.append('REMOVE ' + right)
                else:
                    self.registry.free(right)
                expr_stack.append(left)
                self.next()
                continue

            if self.current()[0] in un_ops:
                left = expr_stack.pop()
                self.registry_command.append(self.current()[0] + ' ' + left)
                expr_stack.append(left)
                self.next()
                continue

            if self.current()[0] in integer:
                reg = self.registry.find_free(self.current()[0])
                value = self.current()[1]
                self.registry_command.append('LOAD ' + reg + ' ' + value)
                expr_stack.append(reg)
                self.next()
                continue

            if self.current()[0] in string:
                reg = self.registry.find_free(self.current()[0])
                value = self.current()[1]
                self.registry_command.append('LOAD ' + reg + ' ' + value)
                expr_stack.append(reg)
                self.next()
                continue

            if self.current()[0] in boolean:
                reg = self.registry.find_free(self.current()[0])
                value = self.current()[1]
                self.registry_command.append('LOAD ' + reg + ' ' + value)
                expr_stack.append(reg)
                self.next()
                continue

            if self.current()[0] == 'VAR':
                reg = self.registry.find_free(self.current()[1])
                value = self.current()[2]
                self.registry_command.append('LOAD ' + reg + ' ' + value)
                expr_stack.append(reg)
                self.next()
                continue

            # if self.current()[0] == 'CALL':
            #     self.next()
            #     self.expr_executor(context=context)
            #     name = str(self.stack.pop())
            #     params = []
            #     self.next()
            #     self.next()
            #     while self.current()[0] != 'ENDPARAM':
            #         self.expr_executor(context=context)
            #         params.append(self.stack.pop()[0])
            #         self.next()
            #     current_index = self.index
            #
            #     if context['variable'][name][1] == 'function':
            #         self.index = self.find_func(name, params)
            #         func_context = deepcopy(self.context)
            #         self.start_execute(func_context)
            #         # expr_stack.append(self.stack.pop())
            #         self.index = current_index
            #         self.context['stack_trace'].pop()
            #         self.next()
            #
            #     if context['variable'][name][1] == list:
            #         index = 1
            #         name, _type, value, array_n = context['variable'][name]
            #         out_of_index = False
            #         if len(params) != len(array_n):
            #             print('Array is %s-dimensional not %s' % (len(array_n), len(params)))
            #             exit(5)
            #         for line, length in params, array_n:
            #             if index > length:
            #                 print('Out of index error %s index %s<%s ' % (context['variable'][name][0],
            #                                                               context['variable'][name][3], len))
            #                 exit(5)
            #             else:
            #                 index += (line - 1) * length
            #
            #         expr_stack.append((*context['variable'][name][2][index], name, index))
            #         # print(expr_stack)
            #         self.next()
            #     continue

            if self.current()[0] == 'ENDEXPR':
                if self.registry.out_reg.state == 'busy':
                    print(WARNING + 'Out register is busy is it normal?' + ENDC)
                self.registry_command.append('ENDEXPR ' + self.registry.out_reg.value + ' ' + expr_stack.pop())
                self.registry.out_reg.state = 'busy'
                self.registry.free_all()
                return self.registry_command

            print('Unexpected expr command %s' % self.current())
            exit(5)
