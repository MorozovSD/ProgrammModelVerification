class lang_identifier:
    """"
    identifier: "[a-zA-Z_][a-zA-Z_0-9]*"; 	// идентификатор
    """
class lang_str:
    """"
    str: "\"[^\"\\]*(?:\\.[^\"\\]*)*\""; 	// строка, окруженная двойными кавычками
    """
class lang_char:
    """"
    char: "'[^']'"; 						// одиночный символ в одинарных кавычках
    """
class lang_hex:
    """"
    hex: "0[xX][0-9A-Fa-f]+"; 				// шестнадцатеричный литерал
    """

class lang_bits:
    """"
    bits: "0[bB][01]+"; 					// битовый литерал
    """
    def f(self):
        return '[a-zA-Z_][a-zA-Z_0-9]*"; 	// идентификатор'
class lang_dec:
    """"
    dec: "[0-9]+"; 							// десятичный литерал
    """
class lang_bool:
    """"
    bool: 'true'|'false'; 					// булевский литерал
    """
class lang_list:
    """"
    list<item>: (item (',' item)*)?; 		// список элементов, разделённых запятыми
    """
