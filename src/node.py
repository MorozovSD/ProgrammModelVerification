from anytree import Node as TreeNode, RenderTree
from anytree.exporter import DotExporter
from subprocess import check_call, CalledProcessError


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

    # def find(self, pattern, node=None):
    #     match = []
    #     if node.children:
    #         for child in node.children:
    #             if child:
    #                 if child.value.name == pattern:
    #                     match += [child]
    #                 if child.children:
    #                     match += self.find(pattern=pattern, node=child)
    #     return match

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
    def __init__(self, role='', pos='', children=None):
        super().__init__(children=children)
        self.pos = pos
        self.role = role

    def __repr__(self):
        return self.role
