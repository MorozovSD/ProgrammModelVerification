from subprocess import check_call, CalledProcessError

from node import Node, NodeValue


class Function:

    @staticmethod
    def get_func(root):
        funcs = []
        funcs += root.find(pattern='funcDef', node=root)
        func_list = []
        for func in funcs:
            func_list += [Function(func)]
        return func_list

    def __init__(self, node):
        self.name = node.find(pattern='funcSignature', node=node)[0].children[0].value.name
        self.statements = Statement(node)


class Statement:

    @staticmethod
    def get_statement(root):
        statement_list = []
        for child in root.children:
            if child:
                if child.value.name == 'statements':
                    statement_list += [*child.children]
        return statement_list

    def __init__(self, node):
        self.statements = self.get_statement(node)

    def build_graph(self, stmt, name, parent=None):
        # def get_next(elem, l):
        #     return l[l.index(elem) + 1] if len(l) >= l.index(elem) + 1 else None
        graph = {}
        root = Graph(GraphValue(name))
        parent = root
        if stmt:
            for statement in stmt:
                if statement:
                    value = statement.value
                    if value.name == 'var':
                        # name, var, type_def, info='', type=''
                        name = value.name
                        var = statement.children[0].children
                        type_def = statement.children[1].children

                        child = Graph(GraphVar(name=name, var=var, type_def=type_def))
                        graph[parent] += [child]
                        # parent.add_child([child])
                        parent = child
                        continue
                    if value.name == 'if':
                        name = value.name
                        stmt_if   = statement.children[0].children
                        stmt_then = statement.children[1].children
                        stmt_else = statement.children[2].children if len(statement.children) == 3 else None
                        if_legs = []

                        if_node = Graph(GraphIf(name=name, stmt_if=stmt_if, stmt_then=stmt_then, stmt_else=stmt_else))
                        # parent.add_child([if_node])
                        graph.update({parent : graph.get(if_node) + [if_node]})
                        graph[parent] += [if_node]

                        then_node = self.build_graph(name='then', stmt=stmt_then)
                        # if_node.add_child([then_node])
                        graph[if_node] += [then_node]
                        graph.update(then_node)
                        # then_last = then_node.find_leaf(if_node)[0] if then_node.find_leaf(if_node) else parent
                        # parent = Graph(GraphValue(name='End if'))
                        # then_last.add_child([parent])
                        # graph[then_last] += [parent]

                        if stmt_else:
                            else_node = self.build_graph(name='else', stmt=stmt_else)
                            # if_node.add_child([else_node])
                            # graph[if_node] += [else_node]
                            # else_last = else_node.find_leaf(if_node)[1] if else_node.find_leaf(if_node) else if_node
                            # else_last.add_child([parent])
                            # graph[else_last] += [parent]
                            graph.update(else_node)

                        continue

                    if value.name == 'while':
                        name = value.name
                        stmt_while = statement.children[0].children
                        stmt_do = statement.children[1].children

                        child = Graph(GraphWhile(name=name, stmt_while=stmt_while, stmt_do=stmt_do))
                        # parent.add_child([child])
                        graph[parent] += [child]
                        parent = child
                        child = self.build_graph(name='do', stmt=stmt_do)
                        # parent.add_child([child])
                        graph.update(child)
                        graph[parent] += [child]
                        # last_do = child.find_leaf(parent)[0] if child.find_leaf(parent) else parent
                        # last_do.add_child([child])
                        # graph[last_do] += [child]
                        continue

                    if value.name == 'do':
                        name = value.name
                        stmt_do = statement.children[0].children
                        stmt_while = statement.children[1].children

                        child = Graph(GraphDo(name=name, stmt_do=stmt_do, stmt_while=stmt_while))
                        # parent.add_child([child])
                        graph[parent] += [child]
                        parent = child
                        child = self.build_graph(name='do', stmt=stmt_do)[0]
                        graph.update(child)
                        graph[parent] += [child]
                        # parent.add_child([child])
                        # graph[parent] += [child]
                        # last_do = child.find_leaf(parent)[0] if child.find_leaf(parent) else parent
                        # last_do.add_child([child])
                        # graph[last_do] += [child]
                        continue

                    if value.name == 'break':
                        name = value.name
                        child = Graph(GraphBreak(name=name))
                        # parent.add_child([child])
                        graph[parent] += [child]
                        parent = child
                        continue

                    if value.name == 'expression':
                        name = value.name
                        expr = statement.children[0].children

                        child = Graph(GraphExpression(name=name, expr=expr))
                        # parent.add_child([child])
                        graph[parent] += [child]
                        parent = child
                        continue
        return graph


class Graph(Node):
    def __repr__(self):
        return str(self.value)

    def dot_exporter(self, node):
        s = self.dot_type(node)
        return 'digraph graphname {\n' + s + '}'

    def to_png(self, tree, filename):
        with open(filename[:-4] + '.dot', 'w', encoding='utf-8') as dotfile:
            dotfile.write(self.dot_exporter(tree))
            dotfile.flush()
            try:
                cmd = ['dot.exe', dotfile.name, '-T', 'png', '-o', filename + '.png']
                print(cmd)
                check_call(cmd)
            except CalledProcessError:
                print('Sorry tree.png wasn\'t created. '
                      'Probably reason: Graphviz don\'t work with some character in node label')

    def dot_type(self, node):
        s = ''
        for child in node.children:
            if child:
                s += '"' + str(node) + '"' + ' -> ' + '"' + str(child) + '"' + ';\n'
                s += self.dot_type(child)
        return s

    def __init__(self, value, children=None):
        super().__init__(value, children)

    def find_leaf(self, node):
        leaf = []
        for child in node.children:
            if child.is_leaf():
                leaf += [child]
            else:
                leaf += self.find_leaf(child)
        return leaf

    def print(self, node, tab='\t'):
        print(tab + str(node))
        if node.children:
            for child in node.children:
                if child:
                    self.print(node=child, tab=tab + '\t')


class GraphValue(NodeValue):
    def __init__(self, name, info='', type=''):
        super().__init__(name, info, type)


class GraphVar(NodeValue):
    def __init__(self, name, var, type_def, info='', type=''):
        super().__init__(name, info, type)
        self.stmt_var = var
        self.stmt_type_def = type_def

    def __repr__(self):
        return 'dim ' + str(self.stmt_var) + ' as ' + str(self.stmt_type_def)


class GraphIf(NodeValue):
    def __init__(self, name, stmt_if, stmt_then, stmt_else=None, info='', type=''):
        super().__init__(name, info, type)
        self.stmt_if = stmt_if
        self.stmt_then = stmt_then
        self.stmt_else = stmt_else

    def __repr__(self):
        return 'if ' + str(self.stmt_if)


class GraphWhile(NodeValue):
    def __init__(self, name, stmt_while, stmt_do, info='', type=''):
        super().__init__(name, info, type)
        self.stmt_while = stmt_while
        self.stmt_do = stmt_do

    def __repr__(self):
        return 'while ' + str(self.stmt_while)


class GraphDo(NodeValue):
    def __init__(self, name, stmt_do, stmt_while, info='', type=''):
        super().__init__(name, info, type)
        self.stmt_while = stmt_while
        self.stmt_do = stmt_do

    def __repr__(self):
        return 'do' + str(self.stmt_while)


class GraphBreak(NodeValue):
    def __init__(self, name, info='', type=''):
        super().__init__(name, info, type)

    def __repr__(self):
        return 'break'


class GraphExpression(NodeValue):
    def __init__(self, name, expr, info='', _type=''):
        super().__init__(name, info, _type)
        self.expr = None
        if type(expr) == list:
            self.expr = []
            for e in expr:
                if e.children:
                    self.expr += [e.children[0].value]
        else:
            self.expr = expr.children[0].value

    def __repr__(self):
        return str(self.expr)

#
# a, b, c, d, e, f, g, h = range(8)
# N = [
# 	{b:2, c:1, d:3, e:9, f:4}, # a
# 	{c:4, e:3}, # b
# 	{d:8}, # c
# 	{e:7}, # d
# 	{f:5}, # e
# 	{c:2, g:2, h:2}, # f
# 	{f:1, h:6}, # g
# 	{f:9, g:8} # h
# ]
