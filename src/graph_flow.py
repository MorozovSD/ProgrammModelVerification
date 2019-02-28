import pprint
from subprocess import check_call, CalledProcessError
from language import *
from node import NodeValue


class Graph:
    @staticmethod
    def to_png(graph, path, name):
        with open(path + name[:-4] + '.dot', 'w', encoding='utf-8') as dotfile:
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
        self.build_graph(func.statements, func)

    def add_value(self, key, value):
        if self.dict.get(key):
            self.dict.update({key: self.dict[key] + [value]})
        else:
            self.dict[key] = [value]

    def build_graph(self, statements, parent=None):
        parent = parent
        if statements:
            for statement in statements:
                if type(statement) in [Break, Declaration, Expression, Assignment]:
                    self.add_value(parent, statement)
                    parent = statement
                    continue

                if type(statement) == Expression:
                    self.add_value(parent, statement)
                    parent = statement
                    continue

                if type(statement) == If:
                    if_start   = NodeValue(role='If', pos=statement.pos)
                    then_start = NodeValue(role='Then', pos=statement.pos)
                    else_start = NodeValue(role='Else', pos=statement.pos)
                    end_if     = NodeValue(role='End if', pos=statement.pos)
                    self.add_value(parent, if_start)
                    self.add_value(if_start, statement.expr)

                    if statement.then_stmt:
                        self.add_value(statement.expr, then_start)
                        then_end = self.build_graph(statement.then_stmt, parent=then_start)
                        self.add_value(then_end, end_if)

                    if statement.else_stmt:
                        self.add_value(statement.expr, else_start)
                        else_end = self.build_graph(statement.else_stmt, parent=else_start)
                        self.add_value(else_end, end_if)

                    if not statement.then_stmt and not statement.else_stmt:
                        self.add_value(if_start, end_if)
                    parent = end_if
                    continue

                if type(statement) == While:
                    if statement.loop_type:
                        loop   = NodeValue(role='Do', pos=statement.pos)
                        end = NodeValue(role='End do', pos=statement.pos)
                        expr = NodeValue(role=statement.loop_type, pos=statement.pos)

                        self.add_value(parent, loop)
                        loop_end = self.build_graph(statement.do_stmt, parent=loop)
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
                        loop_end = self.build_graph(statement.do_stmt, parent=loop)
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
        with open(path + name[:-4] + '.dot', 'w', encoding='utf-8') as dotfile:
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
