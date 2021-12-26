grammar program;

compunit:
	decl EOF
	| funcdef EOF
	| compunit decl EOF
	| compunit funcdef EOF;
decl: constdecl | vardecl;
constdecl: CONST bType constdef ( COMMA constdef)* SEMI;
bType: INT;
constdef: ident (Lsb constexp Rsb)* ASSIGN constinitval;
constinitval:
	constexp
	| Lcb (constinitval ( COMMA constinitval)*)? Rcb;
vardecl: bType vardef ( COMMA vardef)* SEMI;
vardef:
	ident (Lsb constexp Rsb)*					# noassigndef
	| ident (Lsb constexp Rsb)* ASSIGN initval	# assigndef;
initval: exp | Lcb ( initval ( COMMA initval)*)? Rcb;
funcdef: funcType ident Lb (funcfparams)? Rb block;
funcType: VOID | INT;
funcfparams: funcfparam ( COMMA funcfparam)*;
funcfparam: bType ident (Lsb Rsb ( Lsb exp Rsb)*)?;
block: Lcb ( blockitem)* Rcb;
blockitem: decl | stmt;
// stmt: lval ASSIGN exp SEMI # assignstmt | (exp)? SEMI # normalstmt | block # blockstmt | IF Lb
// cond Rb stmt ( ELSE stmt)? # ifstmt | WHILE Lb cond Rb stmt # whilestmt | BREAK SEMI # breakstmt
// | CONTINUE SEMI # continuestmt | RETURN (exp)? SEMI # returnstmt;

stmt:
	assignstmt
	| normalstmt
	| blockstmt
	| ifstmt
	| whilestmt
	| breakstmt
	| continuestmt
	| returnstmt;
assignstmt: lval ASSIGN exp SEMI;
normalstmt: (exp)? SEMI;
blockstmt: block;
ifstmt: IF Lb cond Rb stmt ( ELSE stmt)?;
whilestmt: WHILE Lb cond Rb stmt;
breakstmt: BREAK SEMI;
continuestmt: CONTINUE SEMI;
returnstmt: RETURN (exp)? SEMI;
exp: addexp;
cond: lOrexp;
lval: ident (Lsb exp Rsb)*;
primaryexp:
	Lb exp Rb	# braceexp
	| lval		# lvalexp
	| number	# numberexp;
unaryexp:
	primaryexp
	| ident Lb (funcrparams)? Rb
	| unaryOp unaryexp;
unaryOp: PLUS | MINUS | NOT;
funcrparams: exp ( COMMA exp)*;
mulexp: unaryexp | mulexp (MULTI | DIV | PERCENT) unaryexp;
addexp: mulexp | addexp (PLUS | MINUS) mulexp;
relexp: addexp | relexp (Lab | Rab | LoE | GoE) addexp;
eqexp: relexp | eqexp (Equal | NEqual) relexp;
landexp: eqexp | landexp And eqexp;
lOrexp: landexp | lOrexp Or landexp;
constexp: addexp;
number: Number;
ident: Ident;

LoE: '<=';
GoE: '>=';
Equal: '==';
NEqual: '!=';
And: '&&';
Or: '||';
COMMA: ',';
SEMI: ';';
Lb: '(';
Rb: ')';
Lsb: '[';
Rsb: ']';
Lcb: '{';
Rcb: '}';
Lab: '<';
Rab: '>';
ASSIGN: '=';
PLUS: '+';
MINUS: '-';
MULTI: '*';
DIV: '/';
NOT: '!';
PERCENT: '%';

INT: 'int';
VOID: 'void';
IF: 'if';
ELSE: 'else';
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';
CONST: 'const';

Ident: [_a-zA-Z][a-zA-Z_0-9]*;

Number: Decimal_const | Octal_const | Hexadecimal_const;
Decimal_const: Nonzero_digit Digit*;
Octal_const: '0' Octal_digit*;

Hexadecimal_const: Hexadecimal_prefix Hexadecimal_digit+;
Hexadecimal_prefix: '0x' | '0X';
Nonzero_digit: [1-9];
Octal_digit: [0-7];
Hexadecimal_digit: [0-9] | [a-f] | [A-F];

Digit: [0-9];

Ignore_single: '//' .*? '\r'? '\n' -> skip;
Ignore_multi: '/*' .*? '*/' -> skip;
Blank: (' ' | '\r' | '\n')+ -> skip;

