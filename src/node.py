from tempfile import NamedTemporaryFile

from anytree import Node as TreeNode, RenderTree
from anytree.exporter import DotExporter
from subprocess import check_call
import os
import re


def paint_tree(root, filename):
    with open('tree.dot', 'w') as dotfile:
        for line in DotExporter(root):
            dotfile.write('%s\n' % line)
        dotfile.flush()
        cmd = ['dot.exe', dotfile.name, '-T', 'png', '-o', filename]
        check_call(cmd)


def paint_tree1(root, path):
    DotExporter(root).to_dotfile(path)


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

    def build_tree(self, node=None, parent=None):
        root = TreeNode(node.value, parent=parent if parent else None)
        if node.leaf is not None:
            TreeNode(node.leaf, parent=root)
        for child in node.children:
            if child is not None:
                self.build_tree(node=child, parent=root)
                # if child.leaf is not None:
                #     TreeNode(child.leaf, parent=root)
        return root
