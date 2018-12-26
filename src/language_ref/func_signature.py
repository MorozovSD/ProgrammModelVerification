class FuncSignature:
    """"
    funcSignature: identifier '(' list<argDef> ')' ('as' typeRef)? {
        argDef: identifier ('as' typeRef)?;
    };
    """
    def lang_argDef(self):
        """"
        argDef: identifier ('as' typeRef)?;
        """