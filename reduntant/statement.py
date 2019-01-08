class Statement:
    pass


class expr1:
    pass

class expr2:
    pass

class AssignStatement(Statement):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return 'AssignStatement(%s %s)' % (self.name, self.expr)


class Var(Statement):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'IfStatement(%s)' % self.name


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)


class WhileStatement(Statement):
    class WhileStatement(Statement):
        def __init__(self, condition, body):
            self.condition = condition
            self.body = body

        def __repr__(self):
            return 'WhileStatement(%s, %s)' % (self.condition, self.body)


class Do(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'DoStatement(%s, %s)' % (self.condition, self.body)


class BreakStatement(Statement):
    def __init__(self, const=None):
        self.cosnt = const

    def __repr__(self):
        return 'BreakStatement'


class ExpressionStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
            return 'ExpressionStatement(%s, %s)' % self.expr
