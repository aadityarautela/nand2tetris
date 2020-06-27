import os

class VMWriter(object):
    def __init__(self,fname):
        self.outfile = open(fname, 'w')
    
    def close(self):
        self.outfile.close()
    
    def write_cmd(self, cmd, arg1 = "", arg2 = ""):
        self.outfile.write(cmd + " " + str(arg1) + " " + str(arg2) + "\n")
    
    def write_push(self,seg,index):
        self.write_cmd("push",seg,index)
    
    def write_pop(self,seg,index):
        self.write_cmd("pop",seg,index)
    
    def write_arithmetic(self,cmd):
        self.write_cmd(cmd)
    
    def write_label(self,label):
        self.write_cmd("label",label)
    
    def write_goto(self,label):
        self.write_cmd("goto", label)
    
    def write_if(self,label):
        self.write_cmd("if-goto", label)
    
    def write_call(self,name,nargs):
        self.write_cmd("call",name,nargs)
    
    def write_function(self,name,nlocals):
        self.write_cmd("function",name,nlocals)

    def write_return(self):
        self.write_cmd("return")
    
    #Non Standard i.e. Helper
    def push_const(self,val):
        self.write_push('constant',val)
    
    def push_arg(self, argnum):
        self.write_push('argument', argnum)
        
    def push_this_ptr(self):
        self.write_push('pointer', 0)
        
    def pop_this_ptr(self):
        self.write_pop('pointer', 0)
        
    def pop_that_ptr(self):
        self.write_pop('pointer', 1)
        
    def push_that(self):
        self.write_push('that', 0)
        
    def pop_that(self):
        self.write_pop('that', 0)
        
    def push_temp(self, temp_num):
        self.write_push('temp', temp_num)
        
    def pop_temp(self, temp_num):
        self.write_pop('temp', temp_num)

