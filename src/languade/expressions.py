from languade.statements import Expression
from node import NodeValue


class Brace(Expression):
    def __init__(self, expr, brace=False, pos='', children=None):
        super().__init__(pos=pos, children=children, expr=expr)
        self.brace = brace

    def __repr__(self):
        return '(' + str(self.expr) + ')'


class BinaryExpression(NodeValue):
    def __init__(self, left, right, operand, pos='', children=None):
        super().__init__(pos=pos, children=children)
        self.left = left
        self.right = right
        self.operand = operand

    def __repr__(self):
        return str(self.left) + ' ' + str(self.operand) + ' ' + str(self.right)


class UnaryExpression(NodeValue):
    def __init__(self, expr, operand, pos='', children=None):
        super().__init__(pos=pos, children=children)
        self.expr = expr
        self.operand = operand

    def __repr__(self):
        return self.operand + ' ' + str(self.expr)


class IndexOrParameter(NodeValue):
    def __init__(self, exprs, index, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.exprs = exprs
        self.index = index

    def __repr__(self):
        return str(self.exprs)


class CallOrIndexer(NodeValue):
    def __init__(self, expr, parameters, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.expr = expr
        self.parameters = parameters

    def __repr__(self):
        return self.expr + '(' + str(self.parameters) + ')'
