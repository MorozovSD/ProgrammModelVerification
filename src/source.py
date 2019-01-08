class source:
    pass


class funcSignature(source):
    def __init__(self, name, list):
        self.name = name
        self.list = list

    def __repr__(self):
        return 'funcSignature(%s %s)' % (self.name, self.list)


class sourceItem(source):
    def __init__(self, statement):
        self.statement = statement

    def __repr__(self):
        return 'sourceItem(%s)' % self.statement


