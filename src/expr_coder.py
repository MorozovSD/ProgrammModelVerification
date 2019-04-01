import getopt
import operator
import sys
import os
import ctypes
from copy import deepcopy

WARNING = '\033[93m'
ENDC = '\033[0m'


class Req:
    def __init__(self, state, value):
        self.state = state
        self.value = value

    def free(self):
        self.state = 'free'

    def busy(self):
        self.state = 'busy'


class Registry:
    def __init__(self):
        self.temp_var_id = 0
        self.out = Req('free', '#out')
        self.registry_int = [Req('free', '#i1'),
                             Req('free', '#i2'),
                             Req('free', '#i3'),
                             Req('free', '#i4'),
                             Req('free', '#i5')]

        self.registry_str = [Req('free', '#s1'),
                             Req('free', '#s2'),
                             Req('free', '#s3'),
                             Req('free', '#s4'),
                             Req('free', '#s5')]

        self.registry_bool = [Req('free', '#b1'),
                              Req('free', '#b2'),
                              Req('free', '#b3'),
                              Req('free', '#b4'),
                              Req('free', '#b5')]

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

    def find_free(self, type, registry_command):
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
        registry_command.append('TEMPORARY_LOAD ' + '#TEMP_' + str(self.temp_var_id))
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

string = ['STRING', 'CHAR']
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
        self.registry = Registry()

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
        # print(self.commands)
        while self.current():
            # print(self)
            # print(self.registry_command)
            if self.current()[0] in bin_ops:
                right = expr_stack.pop()
                left = expr_stack.pop()
                to = self.registry.find_free(self.current()[1], self.registry_command)
                self.registry_command.append(self.current()[0] + ' ' + left + ' ' + right + ' ' + to)
                if right[:2] == '#T':
                    self.registry_command.append('REMOVE ' + right)
                else:
                    self.registry.free(right)
                if left[:2] == '#T':
                    self.registry_command.append('REMOVE ' + left)
                else:
                    self.registry.free(left)
                expr_stack.append(to)
                self.next()
                continue

            if self.current()[0] in un_ops:
                left = expr_stack.pop()
                self.registry_command.append(self.current()[0] + ' ' + left)
                expr_stack.append(left)
                self.next()
                continue

            if self.current()[0] in integer:
                reg = self.registry.find_free(self.current()[0], self.registry_command)
                value = self.current()[1]
                self.registry_command.append('LOAD ' + reg + ' ' + value)
                expr_stack.append(reg)
                self.next()
                continue

            if self.current()[0] in string:
                reg = self.registry.find_free(self.current()[0], self.registry_command)
                value = ' '.join(self.current()[1:])
                self.registry_command.append('LOAD ' + reg + ' \'' + value + '\'')
                expr_stack.append(reg)
                self.next()
                continue

            if self.current()[0] in boolean:
                reg = self.registry.find_free(self.current()[0], self.registry_command)
                value = self.current()[1]
                self.registry_command.append('LOAD ' + reg + ' ' + value)
                expr_stack.append(reg)
                self.next()
                continue

            if self.current()[0] == 'VAR':
                reg = self.registry.find_free(self.current()[1], self.registry_command)
                value = self.current()[2]
                self.registry_command.append('VARIABLE_LOAD ' + reg + ' ' + value)
                expr_stack.append(reg)
                self.next()
                continue

            if self.current()[0] == 'CALL':
                # self.registry_command.append('CALL')
                self.next()
                self.registry_command.append('CALL')
                reg_name = self.expr_executor()
                self.registry_command.append('ENDNAME')
                self.next()
                # self.registry_command.append('LOAD ' + reg_name + ' #out')
                params = []
                while self.current()[0] != 'ENDPARAMS':
                    params += self.expr_executor()
                    self.next()

                self.registry_command.append('ENDPARAMS')
                expr_stack.append('#out')
                self.next()

                if reg_name[:2] == '#T':
                    self.registry_command.append('REMOVE ' + reg_name)
                else:
                    self.registry.free(reg_name)

                    # for param in params:
                    #     if param[:2] == '#T':
                    #         self.registry_command.append('REMOVE ' + param)
                    #     else:
                    #         self.registry.free(param)
                continue

            if self.current()[0] == 'ENDEXPR':
                out = expr_stack.pop() if len(expr_stack) else '#out'
                self.registry_command.append('ENDEXPR ' + '#out ' + str(out))

                return self.registry_command

            if self.current()[0] in ['ENDNAME', 'ENDPARAMS']:
                return expr_stack.pop()

            print('Expr decoder:Unexpected expr command %s' % self.current())
            exit(5)
