import re

from anytree import Node, RenderTree
from base_parser import BaseParser
from tree_creator import TreeCreator


class SintaxTreeParser(BaseParser, TreeCreator):
    def variable_parser(self, ver_type, regex):
        identifier = ''
        while re.search(regex, self.current()):
            identifier += self.current()
            self.next()
        if identifier.Length == 0:
            raise Exception("Ожидалось число (pos={0})", self.pos)
        self.skip()
        return Node((ver_type, identifier))

    def parse(self, text, terms):
        """"Parse text to sintax tree"""

        return text

    # def create_node(self):

    # def print(self):
    #     """" Parse text to sintax tree """
    # for pre, fill, node in RenderTree(udo):
    #     print("%s%s" % (pre, node.name))
