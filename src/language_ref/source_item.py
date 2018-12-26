class SourceItem:
    """"
    sourceItem: {
        funcDef: 'function' funcSignature statement* 'end' 'function';
    };
    """
    available_terms = FuncDef_1.available_terms


class FuncDef_1:
    """"
    funcDef: 'function' funcSignature statement* 'end' 'function';
    """
    available_terms = 'function' + funcSignature.available_terms + statement.available_terms + '*' + 'end function'
