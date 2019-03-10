from language import *
from node import NodeValue


class Source(NodeValue):
    def __init__(self, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.source_items = children
        self.source_name = 'Source'
        for child in self.children:
            child.source_name = self.source_name

    def __repr__(self):
        return str(self.source_name)

    def set_source_name(self, name):
        self.source_name = name
        for child in self.children:
            child.source_name = self.source_name

    def get_calls(self):
        calls = {}
        if self.source_items:
            for item in self.source_items:
                calls[item] = item.get(CallOrIndexer)
        return calls

    def get_functions(self):
        return [item for item in self.get(Function)]

    def get_external(self):
        return [item for item in self.get(ExternFunction)]

    def get_class(self):
        return [item for item in self.get(Class)]
