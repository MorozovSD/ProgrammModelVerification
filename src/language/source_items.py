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


class ExternFunction(NodeValue):
    def __init__(self, name, lib_name, alias=None, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.name = name
        self.lib_name = lib_name
        self.alias = alias if alias else name
        self.source_name = None

    def __repr__(self):
        return 'External: ' + str(self.lib_name) + '/' + str(self.name)+ ' as ' + str(self.alias) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return 'External: ' + str(self.lib_name) + '/' + str(self.name) + ' as ' + str(self.alias) + ' (id: ' + self.id + ')'

    def byte_code(self):
        return ['EXFUNC ' + str(self.lib_name), str(self.name), str(self.alias), 'ENDEXFUNC']


class Class(NodeValue):
    def __init__(self, name, members, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.name = name
        self.members = members
        self.source_name = None

    def __repr__(self):
        return 'Class: ' + str(self.name) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return 'Class: ' + str(self.name) + ' (id: ' + self.id + ')'

    def byte_code(self):
        func_stack = ['CLASS ' + str(self.name)]
        for member in filter(None, self.members):
            func_stack += member.byte_code()
        func_stack += ['ECLASS']
        return func_stack

    def get_functions(self):
        functions = []
        for member in self.members:
            if type(member.member) == Function:
                member.member.source_name = self.name
                functions += [member.member]
        return functions

    def get_external(self):
        external = []
        for member in self.members:
            if type(member.member) == ExternFunction:
                member.member.source_name = self.name
                external += [member.member]
        return external


class ClassMember(NodeValue):
    def __init__(self, modifier, member, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.modifier = modifier if modifier else 'public'
        self.member = member
        self.source_name = None

    def __repr__(self):
        return str(self.modifier) + ' ' + str(self.member) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return str(self.modifier) + ' '  + str(self.member) + ' (id: ' + self.id + ')'

    def byte_code(self):
        return ['MEMBER', str(self.modifier), *self.member.byte_code(), 'EMEMBER']