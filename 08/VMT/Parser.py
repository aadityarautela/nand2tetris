import Const


class Parser(object):

    def __init__(self, filename_or_dir):
        isdir = False
        self.file_indexes = []
        if type(filename_or_dir) is list:
            isdir = True
            
        self.commands = []
        if not isdir:
            with open(filename_or_dir, 'r') as f:
                self.commands = f.readlines()
            self.commands = [str.strip(x) for x in self.commands]
            self.commands = [x for x in self.commands if x != '']
            self.commands = [x for x in self.commands if x[0] != '/']
            self.file_indexes.append((filename_or_dir, len(self.commands)-1)) #inclusive range
        else:
            sysvmpath = ""
            for filename in filename_or_dir:
                if filename.endswith("Sys.vm"):
                    sysvmpath = filename
                    break
            with open(sysvmpath, 'r') as f:
                self.commands = f.readlines() 
            self.commands = [str.strip(x) for x in self.commands]
            self.commands = [x for x in self.commands if x != '']
            self.commands = [x for x in self.commands if x[0] != '/']
            self.file_indexes.append((sysvmpath, len(self.commands)-1))
            
            filename_or_dir.remove(sysvmpath)
            
            for filename in filename_or_dir:
                with open(filename, 'r') as f:
                    self.commands += f.readlines()
                self.commands = [str.strip(x) for x in self.commands]
                self.commands = [x for x in self.commands if x != '']
                self.commands = [x for x in self.commands if x[0] != '/']
                self.file_indexes.append((filename, len(self.commands)-1))

        
        self.linum = 0
        self.curr_command = self.commands[self.linum]
        print(self.file_indexes)
    def hasMoreCommands(self):
        if self.linum <= (len(self.commands) - 1):
            return True
        else:
            return False

    def advance(self):
        self.linum = self.linum+1
        try:
            self.curr_command = self.commands[self.linum]
        except:
            pass

    def commandType(self):
        tok_commands = self.curr_command.split()
        return Const.command_types[tok_commands[0]]

    def arg1(self):
        tok_commands = self.curr_command.split()
        if self.commandType() == Const.C_ARITHMETIC:
            return tok_commands[0]
        else:
            return tok_commands[1]

    def arg2(self):
        tok_commands = self.curr_command.split()
        return tok_commands[2]

