from JackConst import *
from JackTokenizer import JackTokenizer
from xml.sax.saxutils import *
import sys

class CompilationEngine(object):
    def __init__(self, infile, outfile):
        self.parsed_rules = []
        self.tokenizer = JackTokenizer(infile)
        self.outfile = open(outfile, 'w')
        self.compile_class()
        self.outfile.close()
    
    def require(self,toktype,val=None):
        tokenizer_toktype, tokenizer_tokval = self.advance()
        print(str(tokenizer_toktype) + ":" + tokenizer_tokval)
        if toktype != tokenizer_toktype or (toktype == T_KEYWORD or toktype == T_SYM) and val != tokenizer_tokval:
            print("Error Parsing")
            sys.exit(0)
        else:
            return tokenizer_tokval
    
    def advance(self):
        toktype, val = self.tokenizer.advance()
        self.write_terminal(toktype,val)
        return toktype,val
    
    def is_token(self,toktype,val=None):
        tokenizer_toktype, tokenizer_tokval = self.tokenizer.peek()
        if val == None:
            return tokenizer_toktype == toktype
        else:
            return (tokenizer_toktype,tokenizer_tokval) == (toktype,val)

    def write_terminal(self,toktype,val):
        self.outfile.write('<'+tokens[toktype]+'> '+escape(val)+' </'+tokens[toktype]+'>\n')

    def start_non_terminal(self,rule):
        self.outfile.write('<'+rule+'>\n')
        self.parsed_rules = [rule] + self.parsed_rules
    
    def end_non_terminal(self):
        rule = self.parsed_rules.pop(0)
        self.outfile.write('</'+rule+'>\n')

    def compile_class(self):
        self.start_non_terminal('class')
        self.require(T_KEYWORD,KW_CLASS)
        class_name = self.require(T_ID)
        self.require(T_SYM,'{')
        while self.is_class_var_dec():
            self.compile_class_var_dec()
        while self.is_subroutine():
            self.compile_subroutine()
        self.require(T_SYM, '}')
        self.end_non_terminal()

    def is_class_var_dec(self):
        return self.is_token(T_KEYWORD,KW_STATIC) or self.is_token(T_KEYWORD,KW_FIELD)
    
    def compile_class_var_dec(self):
        self.start_non_terminal('classVarDec')
        toktype, kword = self.advance()
        self.compile_dec()
        self.end_non_terminal()
    
    def compile_dec(self):
        self.compile_type()
        self.compile_var_name()
        while self.is_token(T_SYM,','):
            self.require(T_SYM,',')
            self.compile_var_name()
        self.require(T_SYM,';')
    
    def is_type(self):
        tokenizer_toktype, tokenizer_tokval = self.tokenizer.peek()
        return tokenizer_toktype == (T_KEYWORD and (tokenizer_tokval == KW_INT or tokenizer_tokval == KW_CHAR or tokenizer_tokval == KW_BOOLEAN)) or tokenizer_toktype == T_ID

    def compile_type(self):
        if self.is_type():
            return self.advance()
    
    def compile_void_or_type(self):
        if self.is_token(T_KEYWORD,KW_VOID):
            return self.advance()
        else:
            return self.compile_type()
    
    def is_var_name(self):
        return self.is_token(T_ID)
    
    def compile_var_name(self):
        self.require(T_ID)
    
    def is_subroutine(self):
        toktype, kwd = self.tokenizer.peek()
        return toktype == T_KEYWORD and (kwd == KW_CONSTRUCTOR or kwd == KW_FUNCTION or kwd == KW_METHOD)
    
    def compile_subroutine(self):
        self.start_non_terminal('subroutineDec')
        kwd = self.advance()
        self.compile_void_or_type()
        self.compile_var_name()
        self.require(T_SYM, '(')
        self.compile_parameter_list()
        self.require(T_SYM, ')')
        self.compile_subroutine_body()
        self.end_non_terminal()
    
    def compile_parameter_list(self):
        self.start_non_terminal('parameterList')
        self.compile_parameter()
        while self.is_token(T_SYM, ','):
            self.advance()
            self.compile_parameter()
        self.end_non_terminal()
    
    def compile_parameter(self):
        if self.is_type():
            self.compile_type()
            self.compile_var_name()

    def compile_subroutine_body(self):
        self.start_non_terminal('subroutineBody')
        self.require(T_SYM,'{')
        while self.is_var_dec():
            self.compile_var_dec()
        self.compile_statements()
        self.require(T_SYM,'}')
        self.end_non_terminal()

    def is_var_dec(self):
        return self.is_token(T_KEYWORD,KW_VAR)
    
    def compile_var_dec(self):
        self.start_non_terminal('varDec')
        self.require(T_KEYWORD,KW_VAR)
        self.compile_dec()
        self.end_non_terminal()

    def compile_statements(self):
        self.start_non_terminal('statements')
        while self.is_statement():
            self.compile_statement()
        self.end_non_terminal()
    
    def is_statement(self):
        return self.is_token(T_KEYWORD,KW_DO) or self.is_token(T_KEYWORD,KW_IF) or self.is_token(T_KEYWORD,KW_LET) or self.is_token(T_KEYWORD,KW_WHILE) or self.is_token(T_KEYWORD,KW_RETURN)  

    def compile_statement(self):
        if self.is_token(T_KEYWORD,KW_DO):
            self.compile_do()
        elif self.is_token(T_KEYWORD,KW_LET):
            self.compile_let()
        elif self.is_token(T_KEYWORD,KW_IF):
            self.compile_if()
        elif self.is_token(T_KEYWORD,KW_WHILE):
            self.compile_while()
        elif self.is_token(T_KEYWORD,KW_RETURN):
            self.compile_return()

    def compile_do(self):
        self.start_non_terminal("doStatement")
        self.require(T_KEYWORD,KW_DO)
        self.require(T_ID)
        self.compile_subroutine_call()
        self.require(T_SYM, ';')
        self.end_non_terminal()

    def compile_let(self):
        self.start_non_terminal('letStatement')
        self.require(T_KEYWORD, KW_LET)
        self.compile_var_name()
        if self.is_token(T_SYM,'['):
            self.advance()
            self.compile_expression()
            self.require(T_SYM,']')
        self.require(T_SYM, '=')
        self.compile_expression()
        self.require(T_SYM,';')
        self.end_non_terminal()
    
    def compile_while(self):
        self.start_non_terminal('whileStatement')
        self.require(T_KEYWORD, KW_WHILE)
        self.compile_conditional_expression_statements()
        self.end_non_terminal()

    def compile_return(self):
        self.start_non_terminal('returnStatement')
        self.require(T_KEYWORD,KW_RETURN)
        if not self.is_token(T_SYM,';'):
            self.compile_expression()
        self.require(T_SYM,';')
        self.end_non_terminal()
    
    def compile_if(self):
        self.start_non_terminal('ifStatement')
        self.require(T_KEYWORD,KW_IF)
        self.compile_conditional_expression_statements()
        if self.is_token(T_KEYWORD,KW_ELSE):
            self.advance()
            self.compile_statements()
        self.end_non_terminal()

    def compile_conditional_expression_statements(self):
        self.require(T_SYM,'(')
        self.compile_expression()
        self.require(T_SYM,')')
        self.require(T_SYM,'{')
        self.compile_statements()
        self.require(T_SYM,'}')
    
    def compile_expression(self):
        if not self.is_term():
            return
        self.start_non_terminal('expression')
        self.compile_term()
        while self.is_op():
            self.advance()
            self.compile_term()
        self.end_non_terminal()

    def is_term(self):
        toktype, val = self.tokenizer.peek()
        isnum = self.is_token(T_NUM)
        isstr = self.is_token(T_STR)
        iskwconst = toktype == T_KEYWORD and val in [KW_TRUE,KW_FALSE,KW_NULL,KW_THIS]
        isvar = self.is_token(T_ID)
        isopenparan = self.is_token(T_SYM, '(')
        isunaryop = self.is_token(T_SYM,'-') or self.is_token(T_SYM, '~')
        return isnum or isstr or iskwconst or isvar or isopenparan or isunaryop

    def compile_term(self):
        self.start_non_terminal('term')
        toktype, val = self.tokenizer.peek()
        if self.is_token(T_NUM) or self.is_token(T_STR) or (toktype == T_KEYWORD and val in [KW_TRUE,KW_FALSE,KW_NULL,KW_THIS]):
            self.advance()
        elif self.is_token(T_SYM,'('):
            self.advance()
            self.compile_expression()
            self.require(T_SYM,')')
        elif self.is_token(T_SYM,'-') or self.is_token(T_SYM,'~'):
            self.advance()
            self.compile_term()
        elif self.is_token(T_ID):
            self.advance()
            if self.is_token(T_SYM,'['):
                self.compile_array_subscript()
            elif self.is_token(T_SYM, '(') or self.is_token(T_SYM,'.'):
                self.compile_subroutine_call()
        self.end_non_terminal()

    def compile_array_subscript(self):
        self.require(T_SYM,'[')
        self.compile_expression()
        self.require(T_SYM,']')

    def compile_subroutine_call(self):
        if self.is_token(T_SYM,'.'):
            self.advance()
            self.require(T_ID)
        self.require(T_SYM,'(')
        self.compile_expression_list()
        self.require(T_SYM,')')
    
    def is_op(self):
        toktype, val = self.tokenizer.peek()
        return toktype == T_SYM and val in '+-*/&|<>='
    
    def compile_expression_list(self):
        self.start_non_terminal('expressionList')
        self.compile_expression()
        while self.is_token(T_SYM,','):
            self.advance()
            self.compile_expression()
        self.end_non_terminal()
