from anytree import Node as TreeNode, RenderTree
from anytree.exporter import DotExporter
from subprocess import check_call, CalledProcessError


def paint_tree(root, filename):
    with open(filename[:-4] + '.dot', 'w', encoding='utf-8') as dotfile:
        for line in DotExporter(root):
            dotfile.write('%s\n' % line)
        dotfile.flush()
        try:
            cmd = ['dot.exe', dotfile.name, '-T', 'png', '-o', filename]
            check_call(cmd)
        except CalledProcessError:
            print('Sorry tree.png wasn\'t created. '
                  'Probably reason: Graphviz don\'t work with some character in node label')


def render_tree(root):
    return RenderTree(root)


class Node:
    def add_children(self, children):
        self.children += children
        return self

    def add_leaf(self, leaf):
        self.leaf += leaf
        return self

    def __repr__(self):
        return str(self.value)

    def __init__(self, value, children=None, leaf=None):
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf


def build_tree(node=None, parent=None):
    root = TreeNode(str(node.value), parent=parent if parent else None)
    if node.leaf is not None:
        if type(node.leaf) == list:
            for leaf in node.leaf:
                TreeNode(leaf, parent=root)
        else:
            TreeNode(node.leaf, parent=root)
    for child in node.children:
        if child is not None:
            build_tree(node=child, parent=root)
            # if child.leaf is not None:
            #     TreeNode(child.leaf, parent=root)
    return root
