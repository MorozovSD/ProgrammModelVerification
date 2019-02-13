from node import NodeValue


class Statements(NodeValue):
    def __init__(self, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'statements'

    def __repr__(self):
        return self.statement_type + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return str(self.statement_type) + ' (id: ' + self.id + ')'


class If(Statements):
    def __init__(self, expr, then_stmt, else_stmt=None, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'if'
        self.expr = expr
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt


class While(Statements):
    def __init__(self, expr, do_stmt, loop_type=None, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'while'
        self.expr = expr
        self.do_stmt = do_stmt
        self.loop_type = loop_type


class Break(Statements):
    def __init__(self, pos=None):
        super().__init__(pos)
        self.statement_type = 'break'


class Assignment(Statements):
    def __init__(self, identifier, expr, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'assignment'
        self.identifier = identifier
        self.expr = expr

    def __repr__(self):
        return str(self.identifier) + ' = ' + str(self.expr) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return str(self.identifier) + ' = ' + str(self.expr) + ' (id: ' + self.id + ')'


class Declaration(Statements):
    def __init__(self, identifiers, pos=None, type=None, children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'dim'
        self.identifiers = identifiers
        self.type = type

    def __repr__(self):
        return self.statement_type + ' ' + str(self.identifiers) + ' as type ' + str(self.type) + ' : Line ' + str(
            self.pos['line'])

    def uniq_str(self):
        return self.statement_type + ' ' + str(self.identifiers) + ' as type ' + str(self.type) + ' (id: ' + self.id + ')'
