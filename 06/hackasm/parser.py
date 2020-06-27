import tokenize
import sys
A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2
NOT_A_COMMAND = 3 

class Parse(object):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    NOT_A_COMMAND = 3 

    def __init__(self,filename):
        self.commands = []
        self.curr_command = ""
        self.linum = 0
        self.tokens = []
        self.curr_token = 1
        with open(filename, 'r') as f:
            self.commands = f.readlines()
        self.commands = [str.strip(x) for x in self.commands]
        self.commands = [x for x in self.commands if x!='']
        self.commands = [x for x in self.commands if x[0]!='/']
        tmp_commands = []
        for cmd in self.commands:
            tmp_cmd = ""
            for letter in cmd:
                if letter == ' ' or letter == '/' or letter == '\t':
                    break
                else:
                    tmp_cmd+=letter
            tmp_commands.append(tmp_cmd)
        self.commands = tmp_commands

        with open(filename+'.bak', 'w') as f:
            f.writelines(["%s\n" %command for command in self.commands])
        with open(filename+'.bak', 'r') as f:
            self.commands = f.readlines()
        with open(filename+'.bak', 'rb') as f:
            tokens = tokenize.tokenize(f.readline)
            for token in tokens:
                self.tokens.append(token)
        self.tokens = [x for x in self.tokens if x.type != tokenize.INDENT]
        self.curr_command = self.commands[0]
        
    def hasMoreCommands(self):
        if self.linum == len(self.commands):
            return False
        return True

    def advance(self):
        hasmorecom = self.hasMoreCommands()
        if hasmorecom:
            self.linum = self.linum + 1
            try:
                self.curr_command = self.commands[self.linum]
                i = self.curr_token
                while self.tokens[i].type != tokenize.NEWLINE:
                    i = i+1
                i = i+1 #To move to next token
                self.curr_token = i
            except:
                pass
            

    def commandType(self):
        if self.curr_command[0] == "@":
            return A_COMMAND
        elif self.curr_command[0] == "(":
            return L_COMMAND
        elif self.curr_command[0] == "/":
            return NOT_A_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        com_type = self.commandType()
        if com_type == A_COMMAND or com_type == L_COMMAND:
            return self.tokens[self.curr_token+1].string

    def dest(self):
        com_type = self.commandType()
        if com_type == C_COMMAND:
            if self.tokens[self.curr_token+1].string == '=':
                return self.tokens[self.curr_token].string
            else:
                return "null"
    
    def jump(self):
        com_type = self.commandType()
        if com_type == C_COMMAND:
            semicolon_token = -1
            i = self.curr_token
            while self.tokens[i].type != tokenize.NEWLINE:
                if self.tokens[i].string == ';':
                    semicolon_token = i
                    break
                else:
                    i=i+1
            if semicolon_token != -1:
                return self.tokens[semicolon_token+1].string
            else:
                return "null"
           
    def comp(self):
        com_type = self.commandType()
        if com_type == C_COMMAND:
            tmp_comp = self.curr_command
            tmp_comp = tmp_comp.replace("\n","")
            dest = self.dest()
            jump = self.jump()
            if dest != "null" and jump != "null":
                tmp_comp = tmp_comp.replace("=","",1)
                tmp_comp = tmp_comp.replace(dest, "",1)
                tmp_comp = tmp_comp.replace(jump, "",1)
                tmp_comp = tmp_comp.replace(";", "",1)
            elif dest != "null" and jump == "null":
                tmp_comp = tmp_comp.replace("=","",1)
                tmp_comp = tmp_comp.replace(dest, "",1)
            elif dest == "null" and jump != "null":
                tmp_comp = self.tokens[self.curr_token].string
            return tmp_comp

    def getSymbol(self):
        sym = self.curr_command.replace("(","")
        sym = sym.replace(")","")
        sym = sym.replace("\n","")
        sym = sym.replace("@", "")
        return sym

#x = Parse("Add1.asm")
#x.advance()
#x.advance()
#print(x.comp())
