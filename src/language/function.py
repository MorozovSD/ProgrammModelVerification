from language import *
from node import NodeValue


class FuncSignature(NodeValue):
    def __init__(self, name, args, pos=None, type=None, children=None, func_type=None):
        super().__init__(pos=pos, children=children)
        self.name = name
        self.args = args if args else ''
        self.type = type
        self.func_type = func_type

    def __repr__(self):
        return 'funcSignature : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return 'funcSignature (id: ' + self.id + ')'


class Function(NodeValue):
    def __init__(self, signature, statements, pos=None, type=None, children=None):
        super().__init__(pos=pos, children=children)
        self.signature = signature
        self.type = type
        self.statements = statements
        self.source_name = None

    def __repr__(self):
        return str(self.source_name) + '/' + str(self.signature.name) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return str(self.source_name) + '/' + str(self.signature.name) + ' (id: ' + self.id + ')'

    def byte_code(self):
        func_stack = ['FUNC ' + str(self.signature.name)]
        if self.statements:
            for statement in filter(None, self.statements):
                func_stack += statement.byte_code()
        func_stack += ['EFUNC']

        return func_stack
