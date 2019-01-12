#
# import lexer
# from tokens import *
# from combinators import *
#
# import source
# import statement
# import expr
#
#
# # def imp_parse(tokens):
# #     ast = parser()(tokens, 0)
# #     return ast
# # def parser():
# #     return parser.Phrase(source_list())
#
# def keyword(kw):
#     return Reserved(kw, RESERVED)
#
#
# id = Tag(ID)
# num = Tag(DEC) ^ (lambda i: int(i))
#
#
# def any_operator_in_list(ops):
#     op_parsers = [keyword(op) for op in ops]
#     parser = reduce(lambda l, r: l | r, op_parsers)
#     return parser
#
#
# def aexp():
#     return precedence(aexp_term(),
#                       aexp_precedence_levels,
#                       process_binop)
# def precedence(value_parser, precedence_levels, combine):
#     def op_parser(precedence_level):
#         return any_operator_in_list(precedence_level) ^ combine
#     parser = value_parser * op_parser(precedence_levels[0])
#     for precedence_level in precedence_levels[1:]:
#         parser = parser * op_parser(precedence_level)
#     return parser
#
# def aexp_value():
#     return (num ^ (lambda i: expr.ExprLiteral(i))) | (id ^ (lambda v: expr.ExprPlace(v)))
#
# def process_relop(parsed):
#     ((left, op), right) = parsed
#     return expr.ExprBinary(op, left, right)
#
# def assign_stmt():
#     def process(parsed):
#         ((name, _), exp) = parsed
#         return statement.AssignStatement(name, exp)
#     return id + keyword('=') + aexp() ^ process
#
# if __name__ == '__main__':
#     print(aexp_value())
