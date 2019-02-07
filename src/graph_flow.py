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

    def add_value(self, dict, key, value):
        if dict.get(key):
            dict.update({key: dict[key] + [value]})
        else:
            dict[key] = [value]

    def build_graph(self, stmt, _parent=None, _graph=None):
        # def get_next(elem, l):
        #     return l[l.index(elem) + 1] if len(l) >= l.index(elem) + 1 else None
        graph = _graph if _graph else {}
        parent = _parent
        if stmt:
            for statement in stmt:
                if statement:
                    value = statement.value
                    if value.name == 'var':
                        var = statement.children[0].children[0].value.name
                        type_def = statement.children[1].children[0].value.name
                        info = StmtInfo(name=value.name,
                                        line=statement.children[0].children[0].value.line,
                                        pos=statement.children[0].children[0].value.pos)

                        child = GraphVar(var=var, type_def=type_def, info=info)
                        self.add_value(graph, parent, child)
                        parent = child
                        continue

                    if value.name == 'break':
                        info = StmtInfo(name=value.name,
                                        line=value.info['line'])
                        child = GraphValue(info=info)
                        graph[parent] = [child]
                        parent = child
                        continue
                    if value.name == 'expression':
                        info = StmtInfo(name=value.name,
                                        line=statement.children[0].value.info['line'])
                        expr = statement
                        child = Graph(GraphExpression(info=info, expr=expr))
                        graph[parent] = [child]
                        parent = child
                        continue
                    # if value.name == 'if':
                    #     name = value.name
                    #     stmt_if = statement.children[0].value
                    #     stmt_then = statement.children[1].children
                    #     stmt_else = statement.children[2].children if len(statement.children) == 3 else None
                    #
                    #     if_start = Graph(GraphValue(name='if'))
                    #     self.add_value(graph, parent, if_start)
                    #     parent = if_start
                    #     if_expr = Graph(GraphExpression(name=name, expr=stmt_if))
                    #     self.add_value(graph, parent, if_expr)
                    #     parent = if_expr
                    #     end_if = Graph(GraphValue(name='End if'))
                    #
                    #     if stmt_then:
                    #         then_start = Graph(GraphValue(name='then'))
                    #         self.add_value(graph, parent, then_start)
                    #         then_parent = then_start
                    #         graph.update(self.build_graph(stmt=stmt_then, _graph=graph, _parent=then_parent))
                    #         then_last = stmt_then[-1]
                    #         self.add_value(graph, then_last, end_if)
                    #         # parent = end_if
                    #
                    #     if stmt_else:
                    #         else_start = Graph(GraphValue(name='else'))
                    #         self.add_value(graph, parent, else_start)
                    #         else_parent = else_start
                    #         graph.update(self.build_graph(stmt=stmt_else, _graph=graph, _parent=else_parent))
                    #         else_last = stmt_else[-1]
                    #         self.add_value(graph, else_last, end_if)
                    #         parent = end_if
                    #
                    #     if not stmt_then and not stmt_else:
                    #         self.add_value(graph, if_expr, end_if)
                    #
                    #     continue
                    #
                    # if value.name == 'while':
                    #     name = value.name
                    #     stmt_while = statement.children[0].children
                    #     stmt_do = statement.children[1].children
                    #     do_node = Graph(GraphWhile(name=name, stmt_while=stmt_while, stmt_do=stmt_do))
                    #     graph[parent] = [do_node]
                    #     graph = self.build_graph(stmt=stmt_do, _graph=graph, _parent=do_node)
                    #     do_last = stmt_do[-1]
                    #     graph.update({do_node: [graph.get(do_node)] + [do_last]})
                    #
                    #     continue
                    #
                    # if value.name == 'do':
                    #     name = value.name
                    #     stmt_do = statement.children[0].children
                    #     stmt_while = statement.children[1].children
                    #
                    #     do_node = Graph(GraphDo(name=name, stmt_do=stmt_do, stmt_while=stmt_while))
                    #     graph[parent] = [do_node]
                    #     graph = self.build_graph(stmt=stmt_do, _graph=graph, _parent=do_node)
                    #     do_last = stmt_do[-1]
                    #     graph.update({do_node: [graph.get(do_node)] + [do_last]})
                    #     continue
                    #

        return graph


class StmtInfo:
    def __init__(self, name, line='', pos=''):
        self.name = name
        self.line = line
        self.pos = pos

    def __repr__(self):
        return self.name + '\n' + '(line:'  + str(self.line) + ')'


class Graph(Node):
    def __repr__(self):
        return str(self.value)

    @staticmethod
    def graph_to_png(graph, filename):
        with open(filename[:-4] + '.dot', 'w', encoding='utf-8') as dotfile:
            dotfile.write(Graph.dot_type(graph))
            dotfile.flush()
            try:
                cmd = ['dot.exe', dotfile.name, '-T', 'png', '-o', filename + '.png']
                print(cmd)
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


class GraphValue:
    def __init__(self, info):
        self.info = info

    def __repr__(self):
        return str(self.info)


class GraphVar(GraphValue):
    def __init__(self, info, var, type_def):
        super().__init__(info)
        self.var_name = var
        self.var_type = type_def

    def __repr__(self):
        return str(self.info) + '\n' \
               'name: '  + str(self.var_name)  + '\n' \
               'type: '  + str(self.var_type)


class GraphExpression(GraphValue):
    # def expr_to_pn(self, expr):
    #     if expr.children:
    #         if expr.children[0].value.name == 'binary':
    #         if expr.children[0].value.name == 'unary':
    #         if expr.children[0].value.name == 'braces':
    #         if expr.children[0].value.name == 'callOrIndexer':
    #         if expr.children[0].value.name == 'place':
    #         if expr.children[0].value.name == 'literal':
    #             self.expr +=
    #     else:
    #         self.expr.append(expr.value.name)
    #         # binary
    #     # unary
    #     # braces
    #     # callOrIndexer
    #     # place
    #     # literal


    def __init__(self, expr, info):
        super().__init__(info)
        self.expr = []
        if type(expr) == Node:
            self.expr_to_pn(expr)
        else:
            self.expr = expr

    def __repr__(self):
        return str(self.expr)

# class GraphIf(GraphValue):
#     def __init__(self, name, stmt_if, stmt_then, stmt_else=None, info='', type=''):
#         super().__init__(info, type)
#         self.stmt_if = stmt_if
#         self.stmt_then = stmt_then
#         self.stmt_else = stmt_else
#
#     def __repr__(self):
#         return 'if ' + str(self.stmt_if)
#
#
# class GraphWhile(GraphValue):
#     def __init__(self, name, stmt_while, stmt_do, info='', type=''):
#         super().__init__(info, type)
#         self.stmt_while = stmt_while
#         self.stmt_do = stmt_do
#
#     def __repr__(self):
#         return 'while ' + str(self.stmt_while)
#
#
# class GraphDo(GraphValue):
#     def __init__(self, name, stmt_do, stmt_while, info='', type=''):
#         super().__init__(info, type)
#         self.stmt_while = stmt_while
#         self.stmt_do = stmt_do
#
#     def __repr__(self):
#         return 'do' + str(self.stmt_while)
#
#

#
#


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
