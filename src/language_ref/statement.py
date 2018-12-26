class lang_statement:
    """"
    statement: {
        |var: 'dim' list<identifier> 'as' typeRef;// for static typing
        |if: 'if' expr 'then' statement* ('else' statement*)? 'end' 'if';
        |while: 'while' expr statement* 'wend';
        |do: 'do' statement* 'loop' ('while'|'until') expr;
        |break: 'break';
        |expression: expr ';';
    };
    """
class lang_var:
    """"
    var: 'dim' list<identifier> 'as' typeRef;// for static typing
    """
class lang_if:
    """"
    if: 'if' expr 'then' statement* ('else' statement*)? 'end' 'if';
    """
class lang_while:
    """"
    while: 'while' expr statement* 'wend';
    """
class lang_do:
    """"
    do: 'do' statement* 'loop' ('while'|'until') expr;
    """
class lang_break:
    """"
        |break: 'break';
    """
class lang_break:
    """"
    expression: expr ';';
    """