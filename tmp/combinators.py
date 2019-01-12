import ply.yacc as yacc


class Result:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Result(%s, %d)' % (self.value, self.pos)


class Parser:
    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens_list, pos):
        if pos < len(tokens_list) and tokens_list[pos][1] is self.tag:
            return Result(tokens_list[pos][0], pos + 1)
        else:
            return None


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens_list, pos):
        if pos < len(tokens_list) and \
                tokens_list[pos][0] == self.value and \
                tokens_list[pos][1] is self.tag:
            return Result(tokens_list[pos][0], pos + 1)
        else:
            return None


class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens_list, pos):
        left_result = self.left(tokens_list, pos)
        if left_result:
            right_result = self.right(tokens_list, left_result.pos)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None


class Exp(Parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens_list, pos):
        result = self.parser(tokens_list, pos)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)

        next_parser = self.separator + self.parser ^ process_next

        next_result = result
        while next_result:
            next_result = next_parser(tokens_list, result.pos)
            if next_result:
                result = next_result
        return result


class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens_list, pos):
        left_result = self.left(tokens_list, pos)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens_list, pos)
            return right_result


class Opt(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens_list, pos):
        result = self.parser(tokens_list, pos)
        if result:
            return result
        else:
            return Result(None, pos)


class Rep(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens_list, pos):
        results = []
        result = self.parser(tokens_list, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens_list, pos)
        return Result(results, pos)


class Process(Parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens_list, pos):
        result = self.parser(tokens_list, pos)
        if result:
            result.value = self.function(result.value)
            return result


class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens_list, pos):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens_list, pos)


class Phrase(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens_list, pos):
        result = self.parser(tokens_list, pos)
        if result and result.pos == len(tokens_list):
            return result
        else:
            return None
