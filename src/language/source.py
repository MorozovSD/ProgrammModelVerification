from node import NodeValue


class Source(NodeValue):
    def __init__(self, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.source_name = 'Source'

    def __repr__(self):
        return str(self.source_name)

