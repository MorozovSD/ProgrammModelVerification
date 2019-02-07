import pprint
from subprocess import check_call, CalledProcessError
from language import *
from node import NodeValue


class Graph:
    def __init__(self, func, path):
        self.dict = {path: ''}
        self.path = path
        self.build_graph(func.statements, path)

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
                    if_start   = NodeValue(role='If')
                    then_start = NodeValue(role='Then')
                    else_start = NodeValue(role='Else')
                    end_if     = NodeValue(role='End if')

                    self.add_value(parent, if_start)
                    self.add_value(if_start, statement.expr)

                    if statement.then_stmt:
                        self.add_value(statement.expr, then_start)
                        self.build_graph(statement.then_stmt, parent=then_start)
                        self.add_value(statement.then_stmt[-1], end_if)
                    if statement.then_stmt:
                        self.add_value(statement.expr, else_start)
                        self.build_graph(statement.else_stmt, parent=else_start)
                        self.add_value(statement.else_stmt[-1], end_if)

                    if not statement.then_stmt and not statement.then_stmt:
                        self.add_value(if_start, end_if)
                    parent = end_if
                    continue

                if type(statement) == While:
                    if statement.loop_type:
                        loop   = NodeValue(role='Do')
                        end = NodeValue(role='End do')
                        expr = NodeValue(role=statement.loop_type)

                        self.add_value(parent, loop)
                        self.build_graph(statement.do_stmt, parent=loop)
                        self.add_value(statement.do_stmt[-1], expr)
                        self.add_value(expr, statement.expr)

                        self.add_value(statement.expr, statement.do_stmt[0])
                        self.add_value(statement.expr, end)
                        parent = end
                    else:
                        expr = NodeValue(role='While')
                        end = NodeValue(role='End while')
                        loop = NodeValue(role='Do')

                        self.add_value(parent, expr)
                        self.add_value(expr, statement.expr)
                        self.add_value(statement.expr, loop)
                        self.build_graph(statement.do_stmt, parent=loop)
                        self.add_value(statement.do_stmt[-1], end)
                        self.add_value(statement.do_stmt[-1], statement.expr)
                        parent = end
                    continue

    def to_png(self, path, name):
        with open(path + name[:-4] + '.dot', 'w', encoding='utf-8') as dotfile:
            dotfile.write(self.dot_type())
            dotfile.flush()
            try:
                cmd = ['dot.exe', dotfile.name, '-T', 'png', '-o', path + name + '.png']
                check_call(cmd)
            except CalledProcessError:
                print('Sorry tree.png wasn\'t created. '
                      'Probably reason: Graphviz don\'t work with some character in node label')

    def dot_type(self):
        s = ''
        for key, value in self.dict.items():
            s += '"' + str(key) + '"[shape=box]\n'
            for v in value:
                s += '"' + str(v) + '"[shape=box]\n'
                s += '"' + str(key) + '" -> "' + str(v) + '"[shape=box];\n'
        return 'digraph graphname {\n' + s + '}'

    def find_leaf(self, node):
        leaf = []
        for child in node.children:
            if child.is_leaf():
                leaf += [child]
            else:
                leaf += self.find_leaf(child)
        return leaf

    def print(self):
        pp = pprint.PrettyPrinter()
        pp.pprint(self.dict)

    def __repr__(self):
        return str(self.dict)
