import CodeWriter, Const, Parser, os, sys

class VMT(object):
    def __init__(self, infile, outfile):
        self.P = Parser.Parser(infile)
        self.C = CodeWriter.CodeWriter(outfile)
    
    def translate(self):
        while self.P.hasMoreCommands():
            if self.P.commandType() == Const.C_ARITHMETIC:
                self.C.writeArithmetic(self.P.curr_command)
            elif self.P.commandType() == Const.C_PUSH:
                self.C.writePushPop(Const.C_PUSH,self.P.arg1(), int(self.P.arg2()))
            elif self.P.commandType() == Const.C_POP:
                self.C.writePushPop(Const.C_POP,self.P.arg1(), int(self.P.arg2()))
            self.P.advance()

if len(sys.argv) < 2:
    print("File not specified!")
    sys.exit(-1)
fname = sys.argv[1]
oname = fname.replace(".vm", ".asm")
V = VMT(fname,oname)
V.translate()
