from expr_coder import ExprCoder
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

    def byte_code(self):
        stmt_stack = []
        then_byte = []
        for stmt in self.then_stmt:
            then_byte += stmt.byte_code()
        expr_byte = ExprCoder([*self.expr.byte_code(), 'ENDEXPR']).expr_executor()

        then_jump = str(len(then_byte) + 4) if self.else_stmt else str(len(then_byte) + 3)

        stmt_stack += ['IF',
                       *expr_byte,
                       'JUMP ' + then_jump]
        stmt_stack += ['BLOCK', *then_byte]

        if self.else_stmt:
            else_byte = []
            for stmt in self.else_stmt:
                else_byte += stmt.byte_code()
            else_jump = str(len(else_byte) + 3)
            stmt_stack += ['JUMP ' + else_jump,
                           'ENDBLOCK',
                           'BLOCK',
                           *else_byte]
        stmt_stack += ['ENDBLOCK']
        return stmt_stack


class While(Statements):
    def __init__(self, expr, do_stmt, loop_type=None, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'while'
        self.expr = expr
        self.do_stmt = do_stmt
        self.loop_type = loop_type

    def byte_code(self):
        stmt_stack = []
        loop_byte = self.expr.byte_code()
        do_byte = []
        for stmt in self.do_stmt:
            do_byte += stmt.byte_code()

        if self.loop_type == 'until':
            loop_byte = ExprCoder([*loop_byte, 'ENDEXPR']).expr_executor()
            stmt_stack += ['LOOP',
                           *do_byte,
                           'IF',
                           *loop_byte,
                           'JUMP -' + str(len(do_byte) + len(do_byte) + 3),
                           'ENDLOOP']
        else:
            loop_byte = ExprCoder([*loop_byte, 'ENDEXPR']).expr_executor()
            stmt_stack += ['LOOP',
                           'IF',
                           *loop_byte,
                           'JUMP ' + str(len(do_byte) + 2),
                           *do_byte,
                           'JUMP -' + str(len(loop_byte) + len(do_byte) + 3),
                           'ENDLOOP']
        return stmt_stack


class Break(Statements):
    def __init__(self, pos=None):
        super().__init__(pos)
        self.statement_type = 'break'

    def byte_code(self):
        return ['BREAK']


class Assignment(Statements):
    def __init__(self, identifiers, expr, pos=None, children=None):
        super().__init__(pos=pos, children=children)
        self.statement_type = 'assignment'
        self.identifiers = identifiers
        self.expr = expr

    def __repr__(self):
        return str(self.identifiers) + ' = ' + str(self.expr) + ' : Line ' + str(self.pos['line'])

    def uniq_str(self):
        return str(self.identifiers) + ' = ' + str(self.expr) + ' (id: ' + self.id + ')'

    def byte_code(self):
        stmt_stack = []
        for id in self.identifiers:
            stmt_stack += ['ASSIGN', *id.byte_code(), *ExprCoder([*self.expr.byte_code(), 'ENDEXPR']).expr_executor()]
        return stmt_stack


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

    def byte_code(self):
        stmt_stack = []
        for id in self.identifiers:
            stmt_stack += ['DIM', *id.byte_code()]
        return stmt_stack
