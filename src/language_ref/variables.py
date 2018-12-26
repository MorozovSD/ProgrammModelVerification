from base_parser import BaseParser
from anytree import Node, RenderTree
import re


class Variables(BaseParser):
    def var_identifier(self):
        """"
        identifier: "[a-zA-Z_][a-zA-Z_0-9]*"; 	// идентификатор
        """
        return 'Identifier', '[a-zA-Z_][a-zA-Z_0-9]*'

    def var_str(self):
        """"
        str: "\"[^\"\\]*(?:\\.[^\"\\]*)*\""; 	// строка, окруженная двойными кавычками
        """
        return 'String', '\"\\\"[^\\\"\\\\]*(?:\\\\.[^\\\"\\\\]*)*\"'

    def var_char(self):
        """"
        char: "'[^']'"; 						// одиночный символ в одинарных кавычках
        """
        return 'Char', '\'[^\']\''

    def var_hex(self):
        """"
        hex: "0[xX][0-9A-Fa-f]+"; 				// шестнадцатеричный литерал
        """
        return 'Hex', '0[xX][0-9A-Fa-f]+'

    def var_bits(self):
        """"
        bits: "0[bB][01]+"; 					// битовый литерал
        """
        return 'Hex', '0[xX][0-9A-Fa-f]+'

    def var_dec(self):
        """"
        dec: "[0-9]+"; 							// десятичный литерал
        """
        return 'Dec', '[0-9]+'

    def var_bool(self):
        """"
        bool: 'true'|'false'; 					// булевский литерал
        """
        return 'Bool', '(true)|(false)'

    # def var_list(self):
    #     """"
    #     list<item>: (item (',' item)*)?; 		// список элементов, разделённых запятыми
    #     """
    #     return 'List', '0[xX][0-9A-Fa-f]+'
