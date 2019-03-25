import sys


class Error(BaseException):
    pass


WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


class VariableTypeException(Exception):
    def __init__(self, expected, actual, pos):
        print(FAIL + 'Unexpected type expected: %s, actual: %s. Position %s' % (expected, actual, pos) + ENDC)
        sys.exit(-1)


class UnknownVariableException(Exception):
    def __init__(self, variable, pos):
        print(FAIL + 'Unknown variable %s. Position %s' % (variable, pos) + ENDC)
        sys.exit(-1)


class BinaryTypeException(Exception):
    def __init__(self, left, right, operand, pos):
        print(FAIL + 'Unexpected binary operand %s, between: %s and %s. Position %s' % (operand, left, right, pos) + ENDC)
        sys.exit(-1)


class UnaryTypeException(Exception):
    def __init__(self, expr, operand, pos):
        print(FAIL + 'Unexpected unary operand %s, for %s. Position %s' % (operand, expr, pos) + ENDC)
        sys.exit(-1)


class NotImplementedYetExeption(Exception):
    def __init__(self, func, node):
        print(FAIL + 'For %s Function %s is not implemented' % (func, node) + ENDC)
        sys.exit(-1)
