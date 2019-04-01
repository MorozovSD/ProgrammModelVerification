from Exeptions import VariableTypeException, UnknownVariableException
from language.expressions import type_comparison, type_conversion
from node import NodeValue


class Literal(NodeValue):
    def __init__(self, value, pos=None, type='', children=None):
        super().__init__(pos=pos, children=children)
        self.value = value
        self.type = type

    def __repr__(self):
        return str(self.value)

    def byte_code(self):
        return [self.type.upper() + ' ' + self.value]

    def get_type(self, context):
        return [self.type]

    def expr_check(self, context, expr_type=None):
        if self.type[:5] == 'ARRAY' or expr_type[:5] == 'ARRAY':
            if expr_type[:5] != self.type[:5]:
                raise VariableTypeException(expected=expr_type, actual=[self.type], pos=self.pos)
        elif expr_type and not type_comparison([self.type], type_conversion[expr_type]):
            raise VariableTypeException(expected=type_conversion[expr_type], actual=[self.type], pos=self.pos)


class Identifier(NodeValue):
    def __init__(self, name, value=None, pos='', type='', children=None):
        super().__init__(pos=pos, children=children)
        self.value = value
        self.type = type
        self.name = name

    def update_type(self, type):
        self.type = type
        return self

    def get_type(self, context):
        self.type = context[self.name].type
        return [self.type]

    def __repr__(self):
        return str(self.name)

    def byte_code(self):
        return ['VAR ' + self.type.upper() + ' ' + self.name]

    def expr_check(self, context, expr_type=None):
        if self.name not in context.keys():
            raise UnknownVariableException(variable=self.name, pos=self.pos)
        self.type = context[self.name].type
        if expr_type and not type_comparison([self.type], type_conversion[expr_type]):
            raise VariableTypeException(expected=type_conversion[expr_type], actual=[self.type], pos=self.pos)


class Argument(NodeValue):
    def __init__(self, identifier, expected_type=None, children=None):
        super().__init__(pos=identifier.pos, children=children)
        self.identifier = identifier
        self.expected_type = expected_type

    def __repr__(self):
        return str(self.identifier.name) + ' as ' + str(self.expected_type)

    def byte_code_dim(self):
        self.identifier.type = self.expected_type.role
        return ['DIM', 'VAR ' + self.expected_type.role.upper() + ' ' + self.identifier.name]

    def byte_code(self):
        param_stack = []
        param_stack += self.byte_code_dim()
        param_stack += self.byte_code_assign()
        return param_stack

    def byte_code_expected_type(self):
        return self.expected_type.role.upper()

    def byte_code_assign(self):
        return ['ASSIGN', *self.identifier.byte_code(), 'POP', 'ENDEXPR #out #out']


class Array(NodeValue):
    def __init__(self, type=None, len=0, children=None):
        super().__init__(children=children)
        self.type = type
        self.len = len
        self.role = 'ARRAY ' + str(len)

    def __repr__(self):
        return 'array of ' + str(self.type)

    def byte_code(self):
        return [str(self.len), *self.type.byte_code()]

    def get_type(self, context):
        return [self.type]

