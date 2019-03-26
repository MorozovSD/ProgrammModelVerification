from anytree import Node as TreeNode, RenderTree
from anytree.exporter import DotExporter

from Exeptions import VariableTypeException, UnknownVariableException, NotImplementedYetExeption


class Node:
    def __repr__(self):
        return 'Node class'

    def __init__(self, children=None):
        self.children = children if children else []

    def is_leaf(self):
        return not bool(self.children)

    def add_child(self, child):
        self.children += child

    def print(self, node, tab='\t'):
        print(tab + str(node))
        if node.children:
            for child in node.children:
                if child:
                    self.print(node=child, tab=tab + '\t')

    def export(self, output_path, name, detailed=False):
        node_for_print = Node.build_tree(node=self)
        tree_for_print = self.render_tree(node_for_print)
        with open(output_path + name + '.txt', 'w', encoding='utf-8') as f:
            for pre, _, node in tree_for_print:
                print("%s%s" % (pre, node.name), file=f)
        if detailed:
            with open(output_path + name + '_detailed' + '.txt', 'w', encoding='utf-8') as f:
                print(tree_for_print, file=f)

    def dot_exporter(self, tree):
        return DotExporter(tree)

    @staticmethod
    def render_tree(root):
        return RenderTree(root)

    @staticmethod
    def build_tree(node=None, parent=None):
        root = TreeNode(str(node), parent=parent if parent else None)
        for child in node.children:
            if child:
                if child.is_leaf():
                    TreeNode(str(child), parent=root)
                else:
                    Node.build_tree(node=child, parent=root)
        return root


class NodeValue(Node):
    def __init__(self, role='', pos=None, children=None):
        super().__init__(children=children)
        self.pos = pos
        self.role = role
        self.context = Context()
        self.id = 'L' + str(pos['line']) + 'P' + str(pos['pos']) if pos else ''

    def __repr__(self):
        pos = ' : ' + str(self.pos['line']) if self.pos else ''
        return str(self.role) + str(pos)

    def get(self, _type):
        list = []
        if self.children:
            for child in self.children:
                if type(child) == _type:
                    list += [child]
        return list

    def get_type(self, context):
        raise NotImplementedYetExeption(func='get_type', node=self)

    def recursive_get(self, _type):
        list = []
        if type(self) == _type:
            list += [self]
        if self.children:
            for child in self.children:
                list += child.recursive_get(_type)
        return list

    # def expr_check_type(self, context, expr_type=None):
    #     from language import Identifier, Literal
    #     # literals_in_expr = self.recursive_get(Literal)
    #     # for literal in literals_in_expr:
    #     #     expr_type = expr_type if expr_type else literal.type
    #     #     if literal.type not in self.type_conversion[expr_type]:
    #     #         raise VariableTypeException(expected=self.type_conversion[expr_type], actual=literal.type, pos=literal.pos)
    #     variables_in_expr = self.recursive_get(Identifier)
    #     for var in variables_in_expr:
    #         if var.name in context.keys():
    #             var_type = context[var.name][1]
    #             # expr_type = expr_type if expr_type else var_type
    #             # if var_type not in self.type_conversion[expr_type]:
    #             #     raise VariableTypeException(expected=self.type_conversion[expr_type], actual=var_type, pos=var.pos)
    #         else:
    #             raise UnknownVariableException(variable=var, pos=var.pos)
    #
    # # def check_valid_type(self, expr_type=None):
    # #     from language import Literal
    # #     literals_in_expr = self.recursive_get(Literal)
    # #     for literal in literals_in_expr:
    # #         expr_type = expr_type if expr_type else literal.type
    # #         if literal.type not in self.type_conversion[expr_type]:
    # #             raise VariableTypeException(expected=expr_type, actual=literal.type, pos=literal.pos)

    def uniq_str(self):
        return str(self) + ' (id: ' + self.id + ')'

    def byte_code(self):
        return [self.role]


class Context:
    def __init__(self, source='', variables=None, functions=None):
        self.source = source
        self.functions = functions or []
        self.variables = variables or []
