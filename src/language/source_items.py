from language import *
from node import NodeValue


class FuncSignature(NodeValue):
    def __init__(self, name, args, pos=None, type='VOID', children=None, func_type='VOID'):
        super().__init__(pos=pos, children=children)
        self.name = name
        self.args = args if args else ''
        self.type = type
        self.func_type = func_type

    def __repr__(self):
        return 'funcSignature : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return 'funcSignature (id: ' + self.id + ')'

    def byte_code(self):
        func_stack = []
        params_type = ''
        if self.args:
            for arg in filter(None, self.args):
                # func_stack += arg.byte_code_dim()
                params_type += str(arg.expected_type.role) + '_'
            # for arg in filter(None, reversed(self.args)):
            #     func_stack += arg.byte_code_assign()
        return ['FUNC ' + str(self.name) + ' ' + params_type.strip('_'), 'DIM', 'VAR ' + self.func_type.upper() + ' ' + str(self.name), *func_stack]


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

    def args(self):
        # params_type = ''
        # if self.signature.args:
        #     for arg in filter(None, self.signature.args):
        #         params_type += str(arg.expected_type.role) + '_'
        # return params_type[:-1] + ' '
        return ' '

    def byte_code(self):
        func_stack = [*self.signature.byte_code()]
        if self.statements:
            for statement in filter(None, self.statements):
                func_stack += statement.byte_code()
        func_stack += ['EXPR', 'LOAD #out ' + self.signature.name,  'ENDEXPR #out #out','EFUNC']

        return func_stack


class ExternFunction(NodeValue):
    def __init__(self, name, args, return_type, lib_name, alias=None, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.name = name
        self.args = args
        self.return_type = return_type
        self.lib_name = lib_name
        self.alias = alias if alias else name
        self.source_name = None

    def __repr__(self):
        return 'External: ' + str(self.lib_name) + '/' + str(self.name) + str(self.args) + ' as ' + str(self.return_type) + 'alias' + str(self.alias) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return 'External: ' + str(self.lib_name) + '/' + str(self.name) + str(self.args) + ' as ' + str(self.return_type) + 'alias' + str(self.alias) + ' (id: ' + self.id + ')'

    def byte_code(self):
        args = ''
        for arg in self.args:
            args += arg.byte_code_expected_type() + ' '
            # args += arg.byte_code_assign()
        return ['EXFUNC ' + str(self.lib_name) + ' ' + str(self.name) + ' ' + str(self.alias) + ' ' + str(self.return_type.role.upper()) + ' ' + args.strip()]


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
