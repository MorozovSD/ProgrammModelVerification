class lang_funcSignature:
    """"
    funcSignature: identifier '(' list<argDef> ')' ('as' typeRef)? {
        argDef: identifier ('as' typeRef)?;
    };
    """
class lang_argDef:
    """"
    argDef: identifier ('as' typeRef)?;
    """