class LangExpr:
    """"
    expr: { // присваивание через '='
        |binary: expr binOp expr; // где binOp - символ бинарного оператора
        |unary: unOp expr; // где unOp - символ унарного оператора
        |braces: '(' expr ')';
        |callOrIndexer: expr '(' list<expr> ')';
        |place: identifier;
        |literal: bool|str|char|hex|bits|dec;
    };
    """
    def lang_binary(self):
        """"
        binary: expr binOp expr; // где binOp - символ бинарного оператора
        """
    def lang_unary(self):
        """"
        unary: unOp expr; // где unOp - символ унарного оператора
        """
    def lang_braces(self):
        """"
        braces: '(' expr ')';
        """
    def lang_callOrIndexer(self):
        """"
        callOrIndexer: expr '(' list<expr> ')';
        """
    def lang_place(self):
        """"
        place: identifier;
        """
    def lang_literal(self):
        """"
        literal: bool|str|char|hex|bits|dec;
        """
