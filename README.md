Задание 1

Цель – освоение верификации синтаксических конструкций текстовых представлений данных.
Реализовать построение по исходному файлу с текстом синтаксического дерева с узлами,
соответствующими правилам варианта, задающего язык для анализа. Вывести полученное дерево
в файл. 

Построить дерево
Вывести в файл


Оформление отчетов
К концу семестра по каждой из работ должен быть представлен отчет, содержащие следующие
части:
1. Цели
2. Задачи
3. Описание работы
4. Аспекты реализации
5. Результаты
6. Выводы 

Вариант:
Типизация   Байт-код    Параметризация
Статическая Регистровый Шаблонизация

Входной язык:

identifier: "[a-zA-Z_][a-zA-Z_0-9]*"; 	// идентификатор

str: "\"[^\"\\]*(?:\\.[^\"\\]*)*\""; 	// строка, окруженная двойными кавычками

char: "'[^']'"; 						// одиночный символ в одинарных кавычках

hex: "0[xX][0-9A-Fa-f]+"; 				// шестнадцатеричный литерал

bits: "0[bB][01]+"; 					// битовый литерал

dec: "[0-9]+"; 							// десятичный литерал

bool: 'true'|'false'; 					// булевский литерал

list<item>: (item (',' item)*)?; 		// список элементов, разделённых запятыми
 
source: sourceItem*;



typeRef: {
 |builtin: 'bool'|'byte'|'int'|'uint'|'long'|'ulong'|'char'|'string';
 
 |custom: identifier;
 
 |array: typeRef '(' (',')* ')';
 
};



funcSignature: identifier '(' list<argDef> ')' ('as' typeRef)? {
 
 argDef: identifier ('as' typeRef)?;
 
};



sourceItem: {

 |funcDef: 'function' funcSignature statement* 'end' 'function';
 
};



statement: {

 |var: 'dim' list<identifier> 'as' typeRef;// for static typing
 
 |if: 'if' expr 'then' statement* ('else' statement*)? 'end' 'if';
 
 |while: 'while' expr statement* 'wend';
 
 |do: 'do' statement* 'loop' ('while'|'until') expr;
 
 |break: 'break';
 
 |expression: expr ';';
 
};


expr: { // присваивание через '='

 |binary: expr binOp expr; // где binOp - символ бинарного оператора
 
 |unary: unOp expr; // где unOp - символ унарного оператора
 
 |braces: '(' expr ')';
 
 |callOrIndexer: expr '(' list<expr> ')';
 
 |place: identifier;
 
 |literal: bool|str|char|hex|bits|dec;
 
}; 


