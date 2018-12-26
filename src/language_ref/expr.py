class lang_expr:
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
class lang_binary:
    """"
    binary: expr binOp expr; // где binOp - символ бинарного оператора
    """
class lang_unary:
    """"
    unary: unOp expr; // где unOp - символ унарного оператора
    """
class lang_braces:
    """"
    braces: '(' expr ')';
    """
class lang_callOrIndexer:
    """"
    callOrIndexer: expr '(' list<expr> ')';
    """
class lang_place:
    """"
    place: identifier;
    """
class lang_literal:
    """"
    literal: bool|str|char|hex|bits|dec;
    """
