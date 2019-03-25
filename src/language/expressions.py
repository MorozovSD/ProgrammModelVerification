from Exeptions import UnknownVariableException, VariableTypeException, BinaryTypeException, UnaryTypeException
from node import NodeValue


class BinOpsType:
    def __init__(self, left, right, result):
        self.left = left
        self.right = right
        self.result = result


class UnOpsType:
    def __init__(self, left, result):
        self.left = left
        self.result = result


def type_comparison(elem, list):
    return set(elem).issubset(list)


int_like = ['dec', 'hex', 'bits', 'int', 'uint', 'long', 'ulong']
str_like = ['string', 'char']
bool_like = ['bool']
type_conversion = {'dec': int_like,
                   'hex': int_like,
                   'bits': int_like,
                   'int': int_like,
                   'uint': int_like,
                   'long': int_like,
                   'ulong': int_like,
                   'string': str_like,
                   'char': str_like,
                   'bool': bool_like}

bin_ops = {'ADD': [BinOpsType(int_like, int_like, int_like),
                   BinOpsType(str_like, str_like, str_like)],

           'MINUS': [BinOpsType(int_like, int_like, int_like)],

           'DIVIDE': [BinOpsType(int_like, int_like, int_like)],

           'MUL': [BinOpsType(int_like, int_like, int_like)],

           'LESSEQ': [BinOpsType(int_like, int_like, bool_like),
                      BinOpsType(str_like, str_like, bool_like),
                      BinOpsType(bool_like, bool_like, bool_like)],

           'LESS': [BinOpsType(int_like, int_like, bool_like),
                    BinOpsType(str_like, str_like, bool_like),
                    BinOpsType(bool_like, bool_like, bool_like)],

           'MOREEQ': [BinOpsType(int_like, int_like, bool_like),
                      BinOpsType(str_like, str_like, bool_like),
                      BinOpsType(bool_like, bool_like, bool_like)],

           'MORE': [BinOpsType(int_like, int_like, bool_like),
                    BinOpsType(str_like, str_like, bool_like),
                    BinOpsType(bool_like, bool_like, bool_like)],

           'NOTEQ': [BinOpsType(int_like, int_like, bool_like),
                     BinOpsType(str_like, str_like, bool_like),
                     BinOpsType(bool_like, bool_like, bool_like)],

           'EQ': [BinOpsType(int_like, int_like, bool_like),
                  BinOpsType(str_like, str_like, bool_like),
                  BinOpsType(bool_like, bool_like, bool_like)],

           'AND': [BinOpsType(bool_like, bool_like, bool_like)],

           'OR': [BinOpsType(bool_like, bool_like, bool_like)]}

un_ops = {'UMINUS': [UnOpsType(int_like, int_like)],
          'NOT': [UnOpsType(bool_like, bool_like)]}


class Expression(NodeValue):
    def __init__(self, expr=None, pos='', children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'expression'
        self.expr = expr

    def __repr__(self):
        return str(self.expr) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return str(self.expr) + ' (id: ' + self.id + ')'

    def byte_code(self):
        return ['EXPR', *self.expr.byte_code(), 'ENDEXPR']

    def check_idendifer(self, context):
        from language import Identifier
        variables_in_expr = self.recursive_get(Identifier)
        for var in variables_in_expr:
            if var.name not in context.keys():
                raise UnknownVariableException(variable=var, pos=var.pos)

    def get_type(self, context):
        return self.expr.get_type(context)

    def expr_check(self, context, expr_type=None):
        self.check_idendifer(context)
        var_type = self.get_type(context)
        if expr_type and not type_comparison(var_type, type_conversion[expr_type]):
            raise VariableTypeException(expected=type_conversion[expr_type], actual=var_type, pos=self.pos)


class Brace(Expression):
    def __init__(self, expr, brace=False, pos='', children=None):
        super().__init__(pos=pos, children=children, expr=expr)
        self.brace = brace

    def __repr__(self):
        return '(' + str(self.expr) + ')'

    def byte_code(self):
        return self.expr.byte_code()

    def get_type(self, context):
        return self.expr.get_type(context)


class BinaryExpression(Expression):
    operands = {'+': 'ADD',
                '-': 'MINUS',
                '/': 'DIVIDE',
                '*': 'MUL',
                'and': 'AND',
                'or': 'OR',
                '<=': 'LESSEQ',
                '<': 'LESS',
                '>=': 'MOREEQ',
                '>': 'MORE',
                '!=': 'NOTEQ',
                '==': 'EQ'}

    def __init__(self, left, right, operand, pos='', children=None):
        super().__init__(pos=pos, children=children)
        self.left = left
        self.right = right
        self.operand = operand

    def get_type(self, context):
        left = self.left.get_type(context)
        right = self.right.get_type(context)

        for bin_ops_type in bin_ops[self.operands[self.operand]]:
            if type_comparison(left, bin_ops_type.left) and type_comparison(right, bin_ops_type.right):
                return bin_ops_type.result
        raise BinaryTypeException(left=left, right=right, operand=self.operand, pos=self.pos)

    def __repr__(self):
        return str(self.left) + ' ' + str(self.operand) + ' ' + str(self.right)

    def byte_code(self):
        return [*self.left.byte_code(), *self.right.byte_code(), self.operands[self.operand]]


class UnaryExpression(Expression):
    operands = {'-': 'UMINUS ',
                'not': 'NOT '}

    def __init__(self, expr, operand, pos='', children=None):
        super().__init__(pos=pos, children=children)
        self.expr = expr
        self.operand = operand

    def __repr__(self):
        return self.operand + str(self.expr)

    def byte_code(self):
        return [*self.expr.byte_code(), self.operands[self.operand]]

    def get_type(self, context):
        expr = self.expr.get_type(context)

        for bin_ops_type in un_ops[self.operands[self.operand]]:
            if type_comparison(expr, bin_ops_type.left):
                return bin_ops_type.result
        raise UnaryTypeException(expr=expr, operand=self.operand, pos=self.pos)


class Parameter(Expression):
    def __init__(self, exprs, index, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.exprs = exprs
        self.index = index

    def __repr__(self):
        return str(self.exprs)

    def byte_code(self):
        return self.exprs.byte_code()


class CallOrIndexer(Expression):
    def __init__(self, path, parameters, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.path = path
        self.parameters = parameters
        from language import Identifier
        self.call_func = None if type(self.path) == Identifier else 'CurrentlyUnknown'

    def __repr__(self):
        return str(self.path) + '(' + str(self.parameters) + ')'

    def byte_code(self):
        parameters = []
        path = []
        for p in self.path:
            path += [*p.byte_code(), 'ENDEXPR']
        for p in self.parameters:
            parameters += [*p.byte_code(), 'ENDEXPR']
        return ['CALL', *path, 'PARAM', *parameters, 'ENDPARAM']


class ExternalVar(Expression):
    def __init__(self, path, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.path = path

    def __repr__(self):
        return str(self.path)

    def byte_code(self):
        path = []
        for p in self.path:
            path += ['EXRP', *p.byte_code(), 'ENDEXPR']
        return ['EXVAR', 'PATH', *path, 'ENDPATH', 'ENDEXVAR']

# class Index(NodeValue):
#     def __init__(self, name, index, pos=None, children=None):
#         super().__init__(pos=pos, children=children)
#         self.name = name
#         self.index = index
#
#     def __repr__(self):
#         return str(self.name) + '(' + str(self.index) + ')'
#
#     def byte_code(self):
#         return ['INDEX', *self.name.byte_code(), *self.index.byte_code(), 'ENDEXPR']
