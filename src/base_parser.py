class BaseParser:
    default_whitespaces = '\n\r\t'
    source = None
    pos = 0

    def __init__(self, source):
        self.source = source
        self.pos = 0

    def current(self):
        return self.source[self.pos]

    def end(self):
        return self.pos == 0

    def next(self):
        if not self.end():
            self.pos += 1

    def skip(self):
        while self.source[self.pos] in self.default_whitespaces:
            self.next()

    def match_no_except(self, terms):
        pos = self.pos
        for term in terms:
            match = True
            for char in term:
                if self.current() == char:
                    self.next()
                else:
                    self.pos = pos
                    match = False
                    break
            if match:
                self.skip()
                return term
        return None

    def is_match(self, terms):
        pos = self.pos
        result = self.match_no_except(terms=terms)
        self.pos = pos
        return result is not None

    def match(self, terms):
        pos = self.pos
        result = self.match_no_except(terms=terms)
        if result is None:
            raise Exception('Expect one of strings %s. Position %s' % (terms, pos))

