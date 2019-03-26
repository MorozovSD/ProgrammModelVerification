import os
import pprint
from copy import deepcopy
from subprocess import check_call, CalledProcessError

from Exeptions import *
from language import *
from language.expressions import type_conversion
from node import NodeValue

class ContextValue:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return str(self.type)

class Graph:
    @staticmethod
    def to_png(graph, path, name):
        filename = path + 'temp/' + name[:-4] + '.dot'
        if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        with open(filename, 'w', encoding='utf-8') as dotfile:
            dotfile.write(Graph.dot_type(graph))
            dotfile.flush()
            try:
                cmd = ['dot.exe', dotfile.name, '-T', 'png', '-o', path + name + '.png']
                check_call(cmd)
            except CalledProcessError:
                print('Sorry tree.png wasn\'t created. '
                      'Probably reason: Graphviz don\'t work with some character in node label')

    @staticmethod
    def dot_type(graph):
        s = ''
        for key, value in graph.items():
            s += '"' + str(key) + '"[shape=box]\n'
            for v in value:
                s += '"' + str(v) + '"[shape=box]\n'
                s += '"' + str(key) + '" -> "' + str(v) + '"[shape=box];\n'
        return 'digraph graphname {\n' + s + '}'

    @staticmethod
    def print(graph):
        pp = pprint.PrettyPrinter()
        pp.pprint(graph)


class GraphFlow(Graph):
    def __init__(self, func, path):
        self.dict = {func: []}
        self.path = path
        self.stack = []
        self.context = {}
        self.build_graph(func.statements, func)

    def add_value(self, key, value):
        if self.dict.get(key):
            self.dict.update({key: self.dict[key] + [value]})
        else:
            self.dict[key] = [value]

    def build_graph(self, statements, parent=None, context=None):
        context = context if context else {}
        parent = parent
        if statements:
            for statement in statements:
                if type(statement) == Break:
                    self.add_value(parent, statement)
                    parent = statement
                    continue

                if type(statement) == Expression:
                    self.add_value(parent, statement)
                    statement.expr_check(context)
                    parent = statement
                    continue

                if type(statement) == Assignment:
                    var_type = ''
                    for id in statement.identifiers:
                        if type(id) == CallOrIndexer:
                            id.expr_check(context)
                            continue

                        id.type = context[id.name].type
                        var_type = var_type if var_type else id.type
                        # arrays
                        if id.type[:5] == 'ARRAY':
                            if var_type[:5] != id.type[:5]:
                                raise VariableTypeException(id.type, var_type, id.pos)

                        elif var_type not in type_conversion[id.type]:
                            raise VariableTypeException(type_conversion[id.type], var_type, id.pos)

                    statement.expr.expr_check(context, var_type)

                    self.add_value(parent, statement)
                    parent = statement
                    continue

                if type(statement) == Declaration:
                    for id in statement.identifiers:
                        if type(statement.type) == Array:
                            id.type = statement.type.role
                        else:
                            id.type = statement.type.role
                        context[id.name] = ContextValue(statement.type.role)
                    self.add_value(parent, statement)
                    parent = statement
                    continue

                if type(statement) == If:
                    if_start   = NodeValue(role='If', pos=statement.pos)
                    then_start = NodeValue(role='Then', pos=statement.pos)
                    else_start = NodeValue(role='Else', pos=statement.pos)
                    end_if     = NodeValue(role='End if', pos=statement.pos)

                    statement.expr.expr_check(context, 'bool')

                    self.add_value(parent, if_start)
                    self.add_value(if_start, statement.expr)

                    if statement.then_stmt:
                        self.add_value(statement.expr, then_start)
                        then_end = self.build_graph(statement.then_stmt, parent=then_start, context=context)
                        self.add_value(then_end, end_if)

                    if statement.else_stmt:
                        self.add_value(statement.expr, else_start)
                        else_end = self.build_graph(statement.else_stmt, parent=else_start, context=context)
                        self.add_value(else_end, end_if)

                    if not statement.then_stmt and not statement.else_stmt:
                        self.add_value(if_start, end_if)
                    parent = end_if
                    continue

                if type(statement) == While:
                    statement.expr.expr_check(context, 'bool')

                    if statement.loop_type:
                        loop   = NodeValue(role='Do', pos=statement.pos)
                        end = NodeValue(role='End do', pos=statement.pos)
                        expr = NodeValue(role=statement.loop_type, pos=statement.pos)

                        self.add_value(parent, loop)
                        loop_end = self.build_graph(statement.do_stmt, parent=loop, context=context)
                        self.add_value(loop_end, expr)
                        self.add_value(expr, statement.expr)

                        self.add_value(statement.expr, loop)
                        self.add_value(statement.expr, end)
                        parent = end
                    else:
                        expr = NodeValue(role='While', pos=statement.pos)
                        end = NodeValue(role='End while', pos=statement.pos)
                        loop = NodeValue(role='Do', pos=statement.pos)

                        self.add_value(parent, expr)
                        self.add_value(expr, statement.expr)
                        self.add_value(statement.expr, loop)
                        loop_end = self.build_graph(statement.do_stmt, parent=loop, context=context)
                        self.add_value(loop_end, end)
                        self.add_value(loop_end, statement.expr)
                        parent = end
                    continue
        return parent

    def print(self):
        pp = pprint.PrettyPrinter()
        pp.pprint(self.dict)

    def __repr__(self):
        return str(self.dict)

    # def to_png(self, path, name):
    #     GraphFlow.to_png(self.dict, path, name)

    def to_png(self, path, name):
        filename = path + 'temp/' + name[:-4] + '.dot'
        if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        with open(filename, 'w', encoding='utf-8') as dotfile:
            dotfile.write(GraphFlow.dot_type(self.dict))
            dotfile.flush()
            try:
                cmd = ['dot.exe', dotfile.name, '-T', 'png', '-o', path + name + '.png']
                check_call(cmd)
            except CalledProcessError:
                print('Sorry tree.png wasn\'t created. '
                      'Probably reason: Graphviz don\'t work with some character in node label')

    @staticmethod
    def dot_type(graph):
        s = ''
        for key, value in graph.items():
            s += '"' + key.uniq_str() + '"[shape=box]\n'
            for v in value:
                s += '"' + v.uniq_str() + '"[shape=box]\n'
                s += '"' + key.uniq_str() + '" -> "' + v.uniq_str() + '"[shape=box];\n'
        return 'digraph graphname {\n' + s + '}'
