import CodeWriter, Const, Parser, os, sys, glob

class VMT(object):
    def __init__(self, infile, outfile):
        self.P = Parser.Parser(infile)
        self.C = CodeWriter.CodeWriter(outfile)
        self.isdir = type(infile) is list
        print(self.P.commands)

    def getStaticName(self,index):
        idx_filename = 0
        for i in range(len(self.P.file_indexes)):
            if self.P.linum <= self.P.file_indexes[i][1]:
                idx_filename = i
            else:
                break
        curr_vm_file = self.P.file_indexes[idx_filename][0]
        slash_idx = 0
        for i in range(len(curr_vm_file)):
            if curr_vm_file[i] == "/":
                slash_idx = i
        curr_vm_file = curr_vm_file[slash_idx+1:]
        curr_vm_file = curr_vm_file.replace(".vm","")
        staticName = curr_vm_file + "." + str(index)
        return staticName

    def translate(self):
        self.C.writeInit(self.isdir)
        while self.P.hasMoreCommands():

            if self.P.commandType() == Const.C_ARITHMETIC:
                self.C.writeArithmetic(self.P.curr_command)
            
            elif self.P.commandType() == Const.C_PUSH:
                if self.P.arg1() != "static":
                    self.C.writePushPop(Const.C_PUSH,self.P.arg1(), int(self.P.arg2()))
                else:
                    self.C.writePushPop(Const.C_PUSH, "static", int(self.P.arg2()), staticName=self.getStaticName(int(self.P.arg2())))

            elif self.P.commandType() == Const.C_POP:
                if self.P.arg1() != "static":
                    self.C.writePushPop(Const.C_POP,self.P.arg1(), int(self.P.arg2()))
                else:
                    self.C.writePushPop(Const.C_POP, "static", int(self.P.arg2()), staticName=self.getStaticName(int(self.P.arg2())))
            
            elif self.P.commandType() == Const.C_CALL:
                self.C.writeCall(self.P.arg1(), int(self.P.arg2()))
            
            elif self.P.commandType() == Const.C_LABEL:
                self.C.writeLabel(self.P.arg1())
            
            elif self.P.commandType() == Const.C_IF:
                self.C.writeIf(self.P.arg1())

            elif self.P.commandType() == Const.C_GOTO:
                self.C.writeGoto(self.P.arg1())
            
            elif self.P.commandType() == Const.C_FUNCTION:
                self.C.writeFunction(self.P.arg1(), int(self.P.arg2()))
            
            elif self.P.commandType() == Const.C_RETURN:
                self.C.writeReturn()

            self.P.advance()

if len(sys.argv) < 2:
    print("File not specified!")
    sys.exit(-1)
fname = sys.argv[1]
oname = ""
if fname.endswith(".vm"):
    oname = fname.replace(".vm", ".asm")
elif not fname.endswith("/"):
    dirname = ""
    tmpindex = -1
    for i in range(len(fname)):
        if fname[i] == "/":
            tmpindex = i
    dirname = fname[tmpindex+1:]
    oname = fname + "/" + dirname +  ".asm"

else:
    dirname = ""
    tmpindex = -1
    for i in range(len(fname)):
        if fname[i] == "/":
            tmpindex = i
    dirname = fname[tmpindex+1:]
    oname = fname + dirname +  ".asm"


if not fname.endswith(".vm"):
    fname = glob.glob(fname + '/*.vm')

V = VMT(fname,oname)
V.translate()
