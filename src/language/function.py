from node import NodeValue


class FuncSignature(NodeValue):
    def __init__(self, name, args, pos=None, type=None, children=None, func_type=None):
        super().__init__(pos=pos, children=children)
        self.name = name
        self.args = args
        self.type = type
        self.func_type = func_type

    def __repr__(self):
        return str('funcSignature') + ' : Line ' + str(self.pos['line'])


class Function(NodeValue):
    def __init__(self, signature, statements, pos=None, type=None, children=None):
        super().__init__(pos=pos, children=children)
        self.signature = signature
        self.type = type
        self.statements = statements
        self.source_name = None

    def __repr__(self):
        return str('funcDef') + ' : Line ' + str(self.pos['line'])
