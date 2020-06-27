import Const
import Parser
import os


class CodeWriter(object):

    def __init__(self, outfile):
        self.outfile = open(outfile, 'w')
        self.vmfile = ''
        self.labelnum = 0
        self.EQCNT = 0
        self.LTCNT = 0
        self.GTCNT = 0

    def setFileName(self, filename):
        self.vmfile, ext = os.path.split(filename)

    def close(self):
        self.outfile.close()

    def writeInit(self, isdir):
        self.outfile.write("// Init\n")
        self.outfile.write("@256\n")
        self.outfile.write("D=A\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=D\n")
        if isdir:
            self.writeCall("Sys.init", 0)
    


    def writeArithmetic(self, command):
        cmd_list = command.split()
        cmd_type = cmd_list[0]

        if cmd_type == "add":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=M+D\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")

        elif cmd_type == "sub":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=M-D\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")

        elif cmd_type == "neg":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=-M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")

        elif cmd_type == "and":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=M&D\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")

        elif cmd_type == "or":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=M|D\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")

        elif cmd_type == "not":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=!M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")

        elif cmd_type == "eq":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M-D\n")
            self.outfile.write("M=-1\n")
            self.outfile.write("@EQ_LABEL_" + str(self.EQCNT) + "\n")
            self.outfile.write("D;JEQ\n")
            self.outfile.write("@SP\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=0\n")
            self.outfile.write("(EQ_LABEL_" + str(self.EQCNT) + ")\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")
            self.EQCNT += 1

        elif cmd_type == "gt":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M-D\n")
            self.outfile.write("M=-1\n")
            self.outfile.write("@GT_LABEL_" + str(self.GTCNT) + "\n")
            self.outfile.write("D;JGT\n")
            self.outfile.write("@SP\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=0\n")
            self.outfile.write("(GT_LABEL_" + str(self.GTCNT) + ")\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")
            self.GTCNT += 1

        elif cmd_type == "lt":
            self.outfile.write("// "+command+"\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M-1\n")
            self.outfile.write("A=M\n")
            self.outfile.write("D=M-D\n")
            self.outfile.write("M=-1\n")
            self.outfile.write("@LT_LABEL_" + str(self.LTCNT) + "\n")
            self.outfile.write("D;JLT\n")
            self.outfile.write("@SP\n")
            self.outfile.write("A=M\n")
            self.outfile.write("M=0\n")
            self.outfile.write("(LT_LABEL_" + str(self.LTCNT) + ")\n")
            self.outfile.write("@SP\n")
            self.outfile.write("M=M+1\n")
            self.LTCNT += 1

    def writePushPop(self, commandtype, segment, index, staticName=None):
        if commandtype == Const.C_PUSH:
            self.outfile.write("// push " + segment + " " + str(index) + "\n")
            if segment == "argument":
                self.outfile.write("@ARG\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("A=A+D\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@SP\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("M=M+1\n")

            elif segment == "local":
                self.outfile.write("@LCL\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("A=A+D\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@SP\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("M=M+1\n")

            elif segment == "static":
                self.outfile.write(
                    "@" + staticName + "\n" + 
                    "D=M\n" + 
                    "@SP\n" +
                    "A=M\n" +
                    "M=D\n" +
                    "@SP\n" +
                    "M=M+1\n"
                )

            elif segment == "constant":
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("D=A\n")
                self.outfile.write("@SP\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("M=M+1\n")

            elif segment == "this":
                self.outfile.write("@THIS\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("A=A+D\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@SP\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("M=M+1\n")

            elif segment == "that":
                self.outfile.write("@THAT\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("A=A+D\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@SP\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("M=M+1\n")

            elif segment == "pointer":
                if index == 0:
                    self.outfile.write("@THIS\n")
                    self.outfile.write("D=M\n")
                    self.outfile.write("@SP\n")
                    self.outfile.write("A=M\n")
                    self.outfile.write("M=D\n")
                    self.outfile.write("@SP\n")
                    self.outfile.write("M=M+1\n")

                else:
                    self.outfile.write("@THAT\n")
                    self.outfile.write("D=M\n")
                    self.outfile.write("@SP\n")
                    self.outfile.write("A=M\n")
                    self.outfile.write("M=D\n")
                    self.outfile.write("@SP\n")
                    self.outfile.write("M=M+1\n")

            elif segment == "temp":
                tmpindex = index+5
                self.outfile.write("@" + str(tmpindex) + "\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@SP\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
                self.outfile.write("D=A+1\n")
                self.outfile.write("@SP\n")
                self.outfile.write("M=D\n")

        else:
            self.outfile.write("// pop " + segment + " " + str(index) + "\n")

            if segment == "argument":
                self.outfile.write("@ARG\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("D=D+A\n")
                self.outfile.write("@R13\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("AM=M-1\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@R13\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
            
            elif segment == "local":
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("D=A\n")
                self.outfile.write("@LCL\n")
                self.outfile.write("D=D+M\n")
                self.outfile.write("@R13\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("M=M-1\n")
                self.outfile.write("A=M\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@R13\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
            
            elif segment == "static":
                self.outfile.write(
                    "@SP\n" + 
                    "M=M-1\n" +
                    "@SP\n" +
                    "A=M\n" +
                    "D=M\n" +
                    "@" + staticName + "\n" +
                    "M=D\n"
                )
            
            elif segment == "this":
                self.outfile.write("@THIS\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("D=D+A\n")
                self.outfile.write("@R13\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("AM=M-1\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@R13\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")

            elif segment == "that":
                self.outfile.write("@THAT\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@" + str(index) + "\n")
                self.outfile.write("D=D+A\n")
                self.outfile.write("@R13\n")
                self.outfile.write("M=D\n")
                self.outfile.write("@SP\n")
                self.outfile.write("AM=M-1\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@R13\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")

            elif segment == "pointer":
                if index == 0:
                    self.outfile.write("@THIS\n")
                    self.outfile.write("D=A\n")
                    self.outfile.write("@R13\n")
                    self.outfile.write("M=D\n")
                    self.outfile.write("@SP\n")
                    self.outfile.write("AM=M-1\n")
                    self.outfile.write("D=M\n")
                    self.outfile.write("@R13\n")
                    self.outfile.write("A=M\n")
                    self.outfile.write("M=D\n")
                else:
                    self.outfile.write("@THAT\n")
                    self.outfile.write("D=A\n")
                    self.outfile.write("@R13\n")
                    self.outfile.write("M=D\n")
                    self.outfile.write("@SP\n")
                    self.outfile.write("AM=M-1\n")
                    self.outfile.write("D=M\n")
                    self.outfile.write("@R13\n")
                    self.outfile.write("A=M\n")
                    self.outfile.write("M=D\n")                    

            elif segment == "temp":
                tmpindex = index + 5
                self.outfile.write("@SP\n")
                self.outfile.write("M=M-1\n")
                self.outfile.write("A=M\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@" + str(tmpindex) + "\n")
                self.outfile.write("M=D\n")

    def newLabel(self):
        self.labelnum += 1
        return "LABEL_" + str(self.labelnum)
    
    def writeLabel(self, label):
        self.outfile.write("// label " + label + "\n")
        self.outfile.write("(" + label + ")\n")
    
    def writeGoto(self, label):
        self.outfile.write("// goto " + label + "\n")
        self.outfile.write("@" + label + "\n")
        self.outfile.write("0;JMP\n")
    
    def writeIf(self,label):
        self.outfile.write("// if-goto " + label + "\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=M-1\n")
        self.outfile.write("A=M\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@" + label  + "\n")
        self.outfile.write("D;JNE\n")

    def writeCall(self,functionName,numArgs):
        self.outfile.write("// call " + functionName + " " +  str(numArgs) + "\n")
        return_addr = self.newLabel()
        self.outfile.write("@" + str(return_addr) + "\n" + "D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        
        self.outfile.write("@LCL\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@SP\n")
        self.outfile.write("A=M\n")
        self.outfile.write("M=D\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=M+1\n")

        self.outfile.write("@ARG\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@SP\n")
        self.outfile.write("A=M\n")
        self.outfile.write("M=D\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=M+1\n")

        self.outfile.write("@THIS\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@SP\n")
        self.outfile.write("A=M\n")
        self.outfile.write("M=D\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=M+1\n")

        self.outfile.write("@THAT\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@SP\n")
        self.outfile.write("A=M\n")
        self.outfile.write("M=D\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=M+1\n")

        self.outfile.write(
                        "@SP\n" +
                        "D=M\n" +
                        "@5\n" +
                        "D=D-A\n" +
                        "@" + str(numArgs) + "\n" +
                        "D=D-A\n" +
                        "@ARG\n" +
                        "M=D\n" +
                        "@SP\n" +
                        "D=M\n" +
                        "@LCL\n" +
                        "M=D\n" +
                        "@" + str(functionName) + "\n" +
                        "0;JMP\n" +
                        "(" + str(return_addr) + ")\n"
                        )

    def writeReturn(self):
        self.outfile.write("// return\n")
        self.outfile.write(
                        "@LCL\n" +
                        "D=M\n" +
                        "@R11\n" +
                        "M=D\n" +
                        "@5\n" +
                        "A=D-A\n" +
                        "D=M\n" +
                        "@R12\n" +
                        "M=D\n"             
        )
        self.outfile.write(
                        "@ARG\n" +
                        "D=M\n" +
                        "@0\n" +
                        "D=D+A\n" +
                        "@R13\n" +
                        "M=D\n" +
                        "@SP\n" +
                        "AM=M-1\n" +
                        "D=M\n" +
                        "@R13\n" +
                        "A=M\n" +
                        "M=D\n"
        )
        self.outfile.write(
                        "@ARG\n" +
                        "D=M\n" +
                        "@SP\n" +
                        "M=D+1\n" 
        )
        self.outfile.write(
                        "@R11\n" +
                        "D=M-1\n" +
                        "AM=D\n" +
                        "D=M\n" +
                        "@THAT\n" +
                        "M=D\n" +
                        "@R11\n" +
                        "D=M-1\n" +
                        "AM=D\n" +
                        "D=M\n" +
                        "@THIS\n" +
                        "M=D\n" +
                        "@R11\n" +
                        "D=M-1\n" +
                        "AM=D\n" +
                        "D=M\n" +
                        "@ARG\n" +
                        "M=D\n" +
                        "@R11\n" +
                        "D=M-1\n" +
                        "AM=D\n" +
                        "D=M\n" +
                        "@LCL\n" +
                        "M=D\n"
        )
        self.outfile.write(
                        "@R12\n" +
                        "A=M\n" +
                        "0;JMP\n"
        )

    def writeFunction(self, functionName, numLocals):
        self.outfile.write("// function " + functionName + " " + str(numLocals) + "\n")
        self.outfile.write("(" + functionName + ")\n")
        for i in range(numLocals):
            self.writePushPop(Const.C_PUSH, "constant", 0)