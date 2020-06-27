from xml.sax.saxutils import escape 
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter
from JackConst import *

class CompilationEngine(object):
    def __init__(self,infile,outfile):
        self.tokenizer = JackTokenizer(infile)
        self.symbols = SymbolTable()
        self.vm = VMWriter(outfile)
        self.label_num = 0
        self.compile_class()
        self.vm.close()
    
    def vm_func_name(self):
        return self.curr_class + '.' + self.curr_subroutine
    
    def vm_push_var(self,name):
        (taipe,kind,index) = self.symbols.lookup(name)
        self.vm.write_push(segments[kind], index)

    def vm_pop_var(self,name):
        (taipe,kind,index) = self.symbols.lookup(name)
        self.vm.write_pop(segments[kind],index)

    def require(self,tok,val=None):
        tokenizer_tok, tokenizer_val = self.advance()
        if tok != tokenizer_tok or (tok in (T_KEYWORD,T_SYM) and val != tokenizer_val):
            print(f"Error Parsing {val} {tokenizer_val} {self.tokenizer.curr_tok_num}")
        else:
            return tokenizer_val
        
    def advance(self):
        return self.tokenizer.advance()

    def is_token(self,tok,val=None):
        tokenizer_tok, tokenizer_val = self.tokenizer.peek()
        return (val == None and tokenizer_tok == tok) or (tokenizer_tok,tokenizer_val) == (tok,val)
    
    def is_keyword(self,*keywords):
        tokenizer_tok, tokenizer_val = self.tokenizer.peek()
        return tokenizer_tok == T_KEYWORD and tokenizer_val in keywords
    
    def is_symbol(self, symbols):
        tokenizer_tok,tokenizer_val = self.tokenizer.peek()
        return tokenizer_tok == T_SYM and tokenizer_val in symbols

    #Main Functions

    def compile_class(self):
        self.require(T_KEYWORD,KW_CLASS)
        self.compile_class_name()
        self.require(T_SYM,'{')
        while self.is_class_var_dec():
            self.compile_class_var_dec()
        while self.is_subroutine():
            self.compile_subroutine()
        self.require(T_SYM,'}')
    
    def compile_class_name(self):
        self.curr_class = self.compile_var_name()
    
    def is_class_var_dec(self):
        return self.is_keyword(KW_STATIC,KW_FIELD)

    def compile_class_var_dec(self):
        tok, kwd = self.advance()
        self.compile_dec(kwd_to_kind[kwd])
    
    def compile_dec(self,kind):
        taipe = self.compile_type()
        name = self.compile_var_name()
        self.symbols.define(name,taipe,kind)
        while self.is_symbol(','):
            self.advance()
            name = self.compile_var_name()
            self.symbols.define(name,taipe,kind)
        self.require(T_SYM,';')
    
    def is_type(self):
        return self.is_token(T_ID) or self.is_keyword(KW_INT,KW_CHAR,KW_BOOLEAN)
    
    def compile_void_or_type(self):
        if self.is_keyword(KW_VOID):
            return self.advance()[1]
        else:
            return self.compile_type()
    
    def compile_type(self):
        if self.is_type():
            return self.advance()[1]
        else:
            print("Error Parsing")

    def is_var_name(self):
        return self.is_token(T_ID)
    
    def compile_var_name(self):
        return self.require(T_ID)

    def is_subroutine(self):
        return self.is_keyword(KW_METHOD,KW_CONSTRUCTOR,KW_FUNCTION)

    def compile_subroutine(self):
        tok, kwd = self.advance()
        taipe = self.compile_void_or_type()
        self.compile_subroutine_name()
        self.symbols.start_subroutine()
        if kwd == KW_METHOD:
            self.symbols.define('this',self.curr_class,SK_ARG)
        self.require(T_SYM,'(')
        self.compile_parameter_list()
        self.require(T_SYM,')')
        self.compile_subroutine_body(kwd)

    def compile_subroutine_name(self):
        self.curr_subroutine = self.compile_var_name()

    def compile_parameter_list(self):
        if self.is_type():
            self.compile_parameter()
            while self.is_symbol(','):
                self.advance()
                self.compile_parameter()
    
    def compile_parameter(self):
        if self.is_type():
            taipe = self.compile_type()
            name = self.compile_var_name()
            self.symbols.define(name,taipe,SK_ARG)
    
    def compile_subroutine_body(self,kwd):
        self.require(T_SYM,'{')
        while self.is_var_dec():
            self.compile_var_dec()
        self.write_function_dec(kwd)
        self.compile_statements()
        self.require(T_SYM,'}')

    def write_function_dec(self,kwd):
        self.vm.write_function(self.vm_func_name(),self.symbols.var_count(SK_VAR))
        self.load_this_ptr(kwd)

    def load_this_ptr(self,kwd):
        if kwd == KW_METHOD:
            self.vm.push_arg(0)
            self.vm.pop_this_ptr()
        elif kwd == KW_CONSTRUCTOR:
            self.vm.push_const(self.symbols.var_count(SK_FIELD))
            self.vm.write_call('Memory.alloc',1)
            self.vm.pop_this_ptr()

    def is_var_dec(self):
        return self.is_keyword(KW_VAR)

    def compile_var_dec(self):
        self.require(T_KEYWORD,KW_VAR)
        return self.compile_dec(SK_VAR)

    def compile_statements(self):
        while self.is_statement():
            self.compile_statement()

    def is_statement(self):
        return self.is_let() or self.is_if() or self.is_while()or self.is_return() or self.is_do()

    def compile_statement(self):
        if self.is_let():
            self.compile_let()
        elif self.is_if():
            self.compile_if()
        elif self.is_while():
            self.compile_while()
        elif self.is_return():
            self.compile_return()
        elif self.is_do():
            self.compile_do()

    def is_let(self):
        return self.is_keyword(KW_LET)
    
    def compile_let(self):
        self.require(T_KEYWORD,KW_LET)
        name = self.compile_var_name()
        sq_bracket = self.is_symbol('[')
        if sq_bracket:
            self.compile_base_plus_index(name)
        self.require(T_SYM,'=')
        self.compile_expression()
        self.require(T_SYM,';')
        if sq_bracket:
            self.pop_array_element()
        else:
            self.vm_pop_var(name)

    def compile_base_plus_index(self,name):
        self.vm_push_var(name)
        self.advance()
        self.compile_expression()
        self.require(T_SYM,']')
        self.vm.write_cmd('add')

    def pop_array_element(self):
        self.vm.pop_temp(TEMP_ARRAY)
        self.vm.pop_that_ptr()
        self.vm.push_temp(TEMP_ARRAY)
        self.vm.pop_that()

    def is_if(self):
        return self.is_keyword(KW_IF)

    def compile_if(self):
        self.require(T_KEYWORD,KW_IF)
        end_label = self.new_label()
        self.compile_conditional_expression_statements(end_label)
        if self.is_keyword(KW_ELSE):
            self.advance()
            self.require(T_SYM,'{')
            self.compile_statements()
            self.require(T_SYM,'}')
        self.vm.write_label(end_label)

    def is_while(self):
        return self.is_keyword(KW_WHILE)

    def compile_while(self):
        self.require(T_KEYWORD,KW_WHILE)
        top_label = self.new_label()
        self.vm.write_label(top_label)
        self.compile_conditional_expression_statements(top_label)

    def compile_conditional_expression_statements(self,label):
        self.require(T_SYM,'(')
        self.compile_expression()
        self.require(T_SYM,')')
        self.vm.write_cmd('not')
        not_if_label = self.new_label()
        self.vm.write_if(not_if_label)
        self.require(T_SYM,'{')
        self.compile_statements()
        self.require(T_SYM,'}')
        self.vm.write_goto(label)
        self.vm.write_label(not_if_label)

    def new_label(self):
        self.label_num += 1
        return 'label' + str(self.label_num)

    def is_do(self):
        return self.is_keyword(KW_DO)

    def compile_do(self):
        self.require(T_KEYWORD,KW_DO)
        name = self.require(T_ID)
        self.compile_subroutine_call(name)
        self.vm.pop_temp(TEMP_RETURN)
        self.require(T_SYM,';')

    def is_return(self):
        return self.is_keyword(KW_RETURN)

    def compile_return(self):
        self.require(T_KEYWORD,KW_RETURN)
        if not self.is_symbol(';'):
            self.compile_expression()
        else:
            self.vm.push_const(0)
        self.require(T_SYM,';')
        self.vm.write_return()

    def compile_expression(self):
        self.compile_term()
        while self.is_op():
            op = self.advance()
            self.compile_term()
            self.vm.write_cmd(vm_cmds[op[1]]) 

    def is_term(self):
        return self.is_const() or self.is_var_name() or self.is_symbol('(') or self.is_unary_op()

    def compile_term(self):
        if self.is_const():
            self.compile_const()
        elif self.is_symbol('('):
            self.advance()
            self.compile_expression()
            self.require(T_SYM,')')
        elif self.is_unary_op():
            tok,op = self.advance()
            self.compile_term()
            self.vm.write_cmd(vm_unary_cmds[op])
        elif self.is_var_name():
            tok,name = self.advance()
            if self.is_symbol('['):
                self.compile_array_subscript(name)
            elif self.is_symbol('(.'):
                self.compile_subroutine_call(name)
            else:
                self.vm_push_var(name)

    def is_const(self):
        return self.is_token(T_NUM) or self.is_token(T_STR) or self.is_keyword_const()

    def is_keyword_const(self):
        return self.is_keyword(KW_THIS,KW_TRUE,KW_FALSE,KW_NULL)

    def is_op(self):
        return self.is_symbol('+-*/&|<>=')

    def is_unary_op(self):
        return self.is_symbol('-~')

    def compile_const(self):
        tok, val = self.advance()
        if tok == T_NUM:
            self.vm.push_const(val)
        elif tok == T_STR:
            self.write_string_const_init(val)
        elif tok == T_KEYWORD:
            self.compile_kwd_const(val)

    def write_string_const_init(self,val):
        self.vm.push_const(len(val))
        self.vm.write_call('String.new',1)
        for c in val:
            self.vm.push_const(ord(c))
            self.vm.write_call('String.appendChar',2)

    def compile_kwd_const(self,kwd):
        if kwd == KW_THIS:
            self.vm.push_this_ptr()
        elif kwd == KW_TRUE:
            self.vm.push_const(1)
            self.vm.write_cmd('neg')
        else:
            self.vm.push_const(0)

    def compile_array_subscript(self,name):
        self.vm_push_var(name)
        self.require(T_SYM,'[')
        self.compile_expression()
        self.require(T_SYM,']')
        self.vm.write_cmd('add')
        self.vm.pop_that_ptr()
        self.vm.push_that()

    def compile_subroutine_call(self,name):
        (taipe,kind,index) = self.symbols.lookup(name)
        if self.is_symbol('.'):
            nargs, name = self.compile_dot_subroutine_call(name,taipe)
        else:
            nargs = 1
            self.vm.push_this_ptr
            name = self.curr_class + '.' + name
        self.require(T_SYM,'(')
        nargs += self.compile_expression_list()
        self.require(T_SYM,')')
        self.vm.write_call(name,nargs)

    def compile_dot_subroutine_call(self,name,taipe):
        nargs = 0
        obj_name = name
        self.advance()
        name = self.compile_var_name()
        if self.is_builtin_type(taipe):
            print("Error")
        elif taipe == None:
            name = obj_name + '.' + name
        else:
            nargs = 1
            self.vm_push_var(obj_name)
            name = self.symbols.type_of(obj_name) + '.' + name 
        return nargs, name

    def is_builtin_type(self,taipe):
        return taipe in [KW_INT,KW_CHAR,KW_BOOLEAN,KW_VOID]

    def compile_expression_list(self):
        nargs = 0
        if self.is_term():
            self.compile_expression()
            nargs = 1
            while self.is_symbol(','):
                self.advance()
                self.compile_expression()
                nargs += 1
        return nargs

    
    

