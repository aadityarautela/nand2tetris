import parser, code, sys, symboltable, os


class Assembler(object):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    NOT_A_COMMAND = 3 

    def __init__(self):
        self.symbols = symboltable.SymbolTable()
        self.sym_addr=16
    
    def first_pass(self,infile):
        p = parser.Parse(infile)
        curr_addr = 0
        while p.hasMoreCommands():
            command = p.commandType()
            if command == self.A_COMMAND or command == self.C_COMMAND:
                curr_addr = curr_addr + 1
            elif command == self.L_COMMAND:
                self.symbols.addEntry(p.getSymbol(),curr_addr)
            p.advance()

    def main_pass(self,infile):
        p = parser.Parse(infile)
        outfilename = infile.replace(".asm", ".hack")
        outfile = open(outfilename, 'w')
        c = code.Code()
        while p.hasMoreCommands():
            command = p.commandType()
            if command == self.A_COMMAND:
                outfile.write(c.genA(self.getAddress(p.getSymbol())) + '\n')
            elif command == self.C_COMMAND:
                outfile.write(c.genC(p.dest(),p.comp(),p.jump()) + '\n')
            p.advance()
    
    def getAddress(self,sym):
        if sym.isdigit():
            return sym
        else:
            if not self.symbols.contains(sym):
                self.symbols.addEntry(sym,self.sym_addr)
                self.sym_addr+=1
            return self.symbols.GetAddress(sym)

    def assemble(self,infile):
        self.first_pass(infile)
        self.main_pass(infile)


if len(sys.argv) != 2:
    raise ValueError("File not specified")
file = sys.argv[1]
asm=Assembler()
asm.assemble(file)
os.remove(file + '.bak')
print("Done")