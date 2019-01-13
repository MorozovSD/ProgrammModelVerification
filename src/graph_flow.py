
class Function:

    @staticmethod
    def get_func(root):
        funcs = []
        funcs += root.find(pattern='funcDef', node=root)
        func_list = []
        for func in funcs:
            func_list += [Function(func)]
        return func_list

    def __init__(self, node):
        self.name = node.find(pattern='funcSignature', node=node)[0].children[0].value.name
        self.statements = Statement(node)


class Statement:

    @staticmethod
    def get_statement(root):
        statement_list = []
        for child in root.children:
            if child.value.name == 'statements':
                statement_list += [*child.children]
        return statement_list

    def __init__(self, node):
        self.statements = self.get_statement(node)


