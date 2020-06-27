T_KEYWORD       = 0
T_SYM           = 1
T_NUM           = 2
T_STR           = 3
T_ID            = 4
T_ERROR         = 5

KW_CLASS        = 'class'
KW_METHOD       = 'method'
KW_FUNCTION     = 'function'
KW_CONSTRUCTOR  = 'constructor'
KW_INT          = 'int'
KW_BOOLEAN      = 'boolean'
KW_CHAR         = 'char'
KW_VOID         = 'void'
KW_VAR          = 'var'
KW_STATIC       = 'static'
KW_FIELD        = 'field'
KW_LET          = 'let'
KW_DO           = 'do'
KW_IF           = 'if'
KW_ELSE         = 'else'
KW_WHILE        = 'while'
KW_RETURN       = 'return'
KW_TRUE         = 'true'
KW_FALSE        = 'false'
KW_NULL         = 'null'
KW_THIS         = 'this'
KW_NONE         = ''

keywords = [KW_CLASS, KW_METHOD, KW_FUNCTION, KW_CONSTRUCTOR, KW_INT, KW_BOOLEAN,
            KW_CHAR, KW_VOID, KW_VAR, KW_STATIC, KW_FIELD, KW_LET, KW_DO, KW_IF,
            KW_ELSE, KW_WHILE, KW_RETURN, KW_TRUE, KW_FALSE, KW_NULL, KW_THIS]


tokens = ['keyword', 'symbol', 'integerConstant', 'stringConstant', 'identifier']


symbols = '{}()[].,;+-*/&|<>=~'

SK_STATIC   = 0
SK_FIELD    = 1
SK_ARG      = 2
SK_VAR      = 3
SK_NONE     = 4

kwd_to_kind = {KW_STATIC:SK_STATIC, KW_FIELD:SK_FIELD}
vm_cmds = {'+':'add', '-':'sub', '*':'call Math.multiply 2', '/':'call Math.divide 2',
           '<':'lt', '>':'gt', '=':'eq', '&':'and', '|':'or'}
vm_unary_cmds = {'-':'neg', '~':'not'}
segments = {SK_STATIC:'static', SK_FIELD:'this', SK_ARG:'argument', SK_VAR:'local', None:'ERROR'} 

TEMP_RETURN = 0
TEMP_ARRAY = 1