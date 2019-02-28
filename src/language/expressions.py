from node import NodeValue


class Expression(NodeValue):
    def __init__(self, expr, pos='', children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'expression'
        self.expr = expr

    def __repr__(self):
        return str(self.expr) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return str(self.expr) + ' (id: ' + self.id + ')'

    def byte_code(self):
        return ['EXPR', *self.expr.byte_code(), 'ENDEXPR']


class Brace(Expression):
    def __init__(self, expr, brace=False, pos='', children=None):
        super().__init__(pos=pos, children=children, expr=expr)
        self.brace = brace

    def __repr__(self):
        return '(' + str(self.expr) + ')'

    def byte_code(self):
        return self.expr.byte_code()


class BinaryExpression(NodeValue):
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

    def __repr__(self):
        return str(self.left) + ' ' + str(self.operand) + ' ' + str(self.right)

    def byte_code(self):
        return [self.operands[self.operand], *self.left.byte_code(), *self.right.byte_code()]


class UnaryExpression(NodeValue):
    operands = {'-': 'UMINUS ',
                'not': 'NOT '}

    def __init__(self, expr, operand, pos='', children=None):
        super().__init__(pos=pos, children=children)
        self.expr = expr
        self.operand = operand

    def __repr__(self):
        return self.operand + str(self.expr)

    def byte_code(self):
        return [self.operands[self.operand], *self.expr.byte_code()]


class Parameter(NodeValue):
    def __init__(self, exprs, index, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.exprs = exprs
        self.index = index

    def __repr__(self):
        return str(self.exprs)

    def byte_code(self):
        return self.exprs.byte_code()


class CallOrIndexer(NodeValue):
    def __init__(self, expr, parameters, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.expr = expr
        self.parameters = parameters
        from language import Identifier
        self.call_func = None if type(self.expr) == Identifier else 'CurrentlyUnknown'

    def __repr__(self):
        return str(self.expr) + '(' + str(self.parameters) + ')'

    def byte_code(self):
        parameters = []
        for p in self.parameters:
            parameters += ['EXPR', *p.byte_code(), 'ENDEXPR']
        return ['CALL', 'EXPR', *self.expr.byte_code(), 'ENDEXPR', 'PARAM', *parameters, 'ENDPARAM']


class Index(NodeValue):
    def __init__(self, name, index, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.name = name
        self.index = index

    def __repr__(self):
        return str(self.name) + '(' + str(self.index) + ')'

    def byte_code(self):
        return ['INDEX', *self.name.byte_code(), 'EXPR',  *self.index.byte_code(), 'ENDEXPR']
