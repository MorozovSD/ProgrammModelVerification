class TypeRef:
    """"
    typeRef: {
        builtin: 'bool'|'byte'|'int'|'uint'|'long'|'ulong'|'char'|'string';
        |custom: identifier;
        |array: typeRef '(' (',')* ')';
    };
    """
    def lang_builtin(self):
        """"
        builtin: 'bool'|'byte'|'int'|'uint'|'long'|'ulong'|'char'|'string';
        """
    def lang_custom(self):
        """"
        custom: identifier;
        """
    def lang_array(self):
        """"
        array: typeRef '(' (',')* ')';
        """