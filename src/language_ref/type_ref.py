class lang_typeRef:
    """"
    typeRef: {
        builtin: 'bool'|'byte'|'int'|'uint'|'long'|'ulong'|'char'|'string';
        |custom: identifier;
        |array: typeRef '(' (',')* ')';
    };
    """
class lang_builtin:
    """"
    builtin: 'bool'|'byte'|'int'|'uint'|'long'|'ulong'|'char'|'string';
    """
class lang_custom:
    """"
    custom: identifier;
    """
class lang_array:
    """"
    array: typeRef '(' (',')* ')';
    """