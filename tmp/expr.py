class expr:
    pass

class ExprBinary(expr):
    def __init__(self, op, expr1, expr2):
        self.op = op
        self.expr1 = expr1
        self.expr2 = expr2

    def __repr__(self):
        return 'ExprBinary(%s, %s, %s)' % (self.op, self.expr1, self.expr2)


class ExprUnary(expr):
    def __init__(self, unary_op, expr1):
        self.unary_op = unary_op
        self.expr1 = expr1

    def __repr__(self):
        return 'ExprUnary(%s, %s)' % (self.unary_op, self.expr1)


class ExprBraces(expr):
    def __init__(self, expr):
        self.open = '('
        self.expr = expr
        self.close = ')'

    def __repr__(self):
        return 'ExprBraces(%s, %s, %s)' % (self.open, self.expr, self.close)


class ExprCallOrIndexer(expr):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.open = '('
        self.expr2 = expr2
        self.close = ')'
        self.list = 'list'
        self.list_type_open = '<'
        self.list_type_close = '>'

    def __repr__(self):
        return 'ExprCallOrIndexer(%s, %s, %s, %s, %s, %s, %s)' % (self.expr1, self.open, self.list, self.list_type_open,
                                                                  self.expr2, self.list_type_close, self.close)


class ExprPlace(expr):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return 'ExprPlace(%s)' % self.identifier


class ExprLiteral(expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'ExprLiteral(%s)' % self.value
