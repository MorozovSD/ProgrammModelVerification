from node import NodeValue


class Literal(NodeValue):
    def __init__(self, value, pos=None, type='', children=None):
        super().__init__(pos=pos, children=children)
        self.value = value
        self.type = type

    def __repr__(self):
        return str(self.value)

    def byte_code(self):
        return [self.type.upper(), self.value]


class Identifier(NodeValue):
    def __init__(self, name, value=None, pos='', type=None, children=None):
        super().__init__(pos=pos, children=children)
        self.value = value
        self.type = type
        self.name = name

    def update_type(self, type):
        self.type = type
        return self

    def __repr__(self):
        return str(self.name)

    def byte_code(self):
        return ['VAR ' + self.name]


class Argument(NodeValue):
    def __init__(self, identifier, expected_type=None, children=None):
        super().__init__(pos=identifier.pos, children=children)
        self.identifier = identifier
        self.expected_type = expected_type

    def __repr__(self):
        return str(self.identifier.name) + ' as ' + str(self.expected_type)

    def byte_code_dim(self):
        return ['DIM', *self.identifier.byte_code(), *self.expected_type.byte_code()]

    def byte_code_assign(self):
        return ['ASSIGN', *self.identifier.byte_code(), 'POP', 'ENDEXPR']


class Array(NodeValue):
    def __init__(self, type=None, len=0, children=None):
        super().__init__(children=children)
        self.type = type
        self.len = len

    def __repr__(self):
        return 'array of ' + str(self.type)

    def byte_code(self):
        return ['ARRAY', str(self.len), *self.type.byte_code()]
