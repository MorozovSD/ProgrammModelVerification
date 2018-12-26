class Statement:
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
    def lang_var(self):
        """"
        var: 'dim' list<identifier> 'as' typeRef;// for static typing
        """
    def lang_if(self):
        """"
        if: 'if' expr 'then' statement* ('else' statement*)? 'end' 'if';
        """
    def lang_while(self):
        """"
        while: 'while' expr statement* 'wend';
        """
    def lang_do(self):
        """"
        do: 'do' statement* 'loop' ('while'|'until') expr;
        """
    def lang_break(self):
        """"
            |break: 'break';
        """
    def lang_break(self):
        """"
        expression: expr ';';
        """