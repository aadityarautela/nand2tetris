from JackConst import *

class SymbolTable(object):
    def __init__(self):
        self.class_symbols = {}
        self.subroutine_symbols = {}
        self.symbols = {SK_STATIC:self.class_symbols, SK_FIELD:self.class_symbols,SK_ARG:self.subroutine_symbols, SK_VAR:self.subroutine_symbols}
        self.index = {SK_STATIC:0, SK_FIELD:0, SK_ARG:0,SK_VAR:0}
    
    def start_subroutine(self):
        self.subroutine_symbols.clear()
        self.index[SK_ARG] = 0
        self.index[SK_VAR] = 0
    
    def define(self,name,taipe,kind):
        self.symbols[kind][name] = (taipe,kind,self.index[kind])
        self.index[kind] += 1
    
    def var_count(self,kind):
        return len(self.symbols[kind])
    
    def lookup(self,name):
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name]
        elif name in self.class_symbols:
            return self.class_symbols[name]
        else:
            return (None,None,None)
    
    def kind_of(self,name):
        (taipe,kind,index) = self.lookup(name)
        return kind

    def type_of(self,name):
        (taipe,kind,index) = self.lookup(name)
        return taipe    