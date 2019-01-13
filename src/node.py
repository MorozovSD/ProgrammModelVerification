from anytree import Node as TreeNode, RenderTree
from anytree.exporter import DotExporter
from subprocess import check_call, CalledProcessError


class Node:
    def __repr__(self):
        return str(self.value)

    def __init__(self, value, children=None):
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []
    
    def is_leaf(self):
        return not bool(self.children)
        # self.leaf = leaf

    # def find(self, pattern, node=None):
    #     l = []
    #     if node.children:
    #         for child in node.children:
    #             if child :
    #                 if child.value.name == pattern:
    #                     l += [child]
    #                 if child.children :
    #                     l += self.find(pattern=pattern, node=child)
    #     return l
    def print(self, node, tab='\t'):
        print(tab + node.value.name)
        if node.children:
            for child in node.children:
                if child:
                    self.print(node=child, tab=tab+'\t')

    def find(self, pattern, node=None):
        match = []
        if node.children:
            for child in node.children:
                if child:
                    if child.value.name == pattern:
                        match += [child]
                    if child.children:
                        match += self.find(pattern=pattern, node=child)
        return match

    def update_func_names(self, pattern, value, node=None):
        match = []
        if node.children:
            for child in node.children:
                if child:
                    if child.value.name == pattern:
                        founded = child
                        founded.children[0].value.name = value + founded.children[0].value.name
                        match += [founded]
                    if child.children:
                        match += self.update_func_names(pattern=pattern, node=child, value=value)
        return match

    def export(self, output_path, name, to_image=True, detailed=False):
        node_for_print = Node.build_tree(node=self)
        tree_for_print = self.render_tree(node_for_print)
        if to_image:
            Node.to_png(node_for_print, output_path + name + '.png')
        with open(output_path + name + '.txt', 'w', encoding='utf-8') as f:
            for pre, _, node in tree_for_print:
                print("%s%s" % (pre, node.name), file=f)
        if detailed:
            with open(output_path + name + '_detailed' + '.txt', 'w', encoding='utf-8') as f:
                print(tree_for_print, file=f)

    @staticmethod
    def to_png(tree, filename):
        with open(filename[:-4] + '.dot', 'w', encoding='utf-8') as dotfile:
            for line in DotExporter(tree):
                dotfile.write('%s\n' % line)
            dotfile.flush()
            try:
                cmd = ['dot.exe', dotfile.name, '-T', 'png', '-o', filename]
                check_call(cmd)
            except CalledProcessError:
                print('Sorry tree.png wasn\'t created. '
                      'Probably reason: Graphviz don\'t work with some character in node label')

    @staticmethod
    def render_tree(root):
        return RenderTree(root)

    @staticmethod
    def build_tree(node=None, parent=None):
        root = TreeNode(str(node.value), parent=parent if parent else None)
        for child in node.children:
            if child:
                if child.is_leaf():
                    TreeNode(str(child.value), parent=root)
                else:
                    Node.build_tree(node=child, parent=root)
        return root


class NodeValue:
    count = {}

    @staticmethod
    def set_info(p, pos=1):
        return {'line': str(p.lineno(pos))}

    @staticmethod
    def set_name(p, pos=0):
        return p.slice[pos].type

    @staticmethod
    def find_column(data, pos):
        line_start = data.rfind('\n', 0, pos) + 1
        return (pos - line_start) + 1

    def __init__(self, name, info='', type=''):
        if name in self.count:
            NodeValue.count[name] += 1
        else:
            NodeValue.count[name] = 1
        self.count = NodeValue.count[name]
        self.name = name
        self.type = type
        self.info = info

    def __repr__(self):
        type = str(self.type) + ' : ' if self.type else ''
        return type + str(self.name) + '(' + str('id: ' + str(self.count)) + ')'

    def set_type(self, type):
        self.type = type
        return self


class LeafValue(NodeValue):
    def __init__(self, p, name, type='', index=1, info='', replace=''):
        super().__init__(name, info)
        self.type = type
        self.name = p[index].replace(replace, '')
        self.pos = NodeValue.find_column(p.lexer.lexdata, p.lexpos(index))
        self.line = p.lineno(index)
        self.info = info

    def __repr__(self):
        type = str(self.type) + ' : ' if self.type else ''
        return type + str(self.name) + str(('line: ' + str(self.line), 'pos: ' + str(self.pos)))
