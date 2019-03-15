from anytree import Node as TreeNode, RenderTree
from anytree.exporter import DotExporter


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
        return self.role + pos

    def get(self, _type):
        list = []
        if self.children:
            for child in self.children:
                if type(child) == _type:
                    list += [child]
        return list

    def recursive_get(self, _type):
        list = []
        if type(self) == _type:
            list += [self]
        if self.children:
            for child in self.children:
                list += child.recursive_get(_type)
        return list

    def uniq_str(self):
        return str(self) + ' (id: ' + self.id + ')'

    def byte_code(self):
        return [self.role]


class Context:
    def __init__(self, source='', variables=None, functions=None):
        self.source = source
        self.functions = functions or []
        self.variables = variables or []
