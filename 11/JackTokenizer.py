import tokenize
from JackConst import *

class JackTokenizer(object):
    def __init__(self,filename):
        toks = []
        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()
        tmplines = []
        for line in lines:
            tmpline = line.strip()
            if tmpline == "":
                pass
            elif not (tmpline[0] == '/' or tmpline[0] == '*'):
                tmplines.append(tmpline + "\n")
        with open(filename + ".tmp", 'w') as f:
            f.writelines(tmplines)
        with open(filename + ".tmp", 'r') as f:
            tmp = tokenize.generate_tokens(f.readline)
            for tok in tmp:
                toks.append(tok.string)
        for i in range(len(toks)):
            if toks[i] == "/":
                if toks[i+1] == "*" or toks[i+1] == "**":
                    toks[i] = "/**"
                    toks[i+1] = ""
            elif toks[i] == "*":
                if toks[i+1] == "/":
                    toks[i] = "*/"
                    toks[i+1] = ""
        skip = False
        nl = False
        for i in range(len(toks)):
            if toks[i] == "//":
                skip = True
            elif toks[i] == "\n":
                nl = True
            
            if nl:
                nl = False
                skip = False
                toks[i] = ""
            elif skip:
                toks[i] = ""
                continue
        skip = False
        comment_end = False
        for i in range(len(toks)):
            if toks[i] == "/**" or toks[i] == "/*":
                skip = True
            elif toks[i] == "*/":
                comment_end = True
                skip = True
            if comment_end:
                toks[i] = ""
                comment_end = False
                skip = False
            elif skip:
                toks[i] = ""
        self.tokens = []
        for tok in toks:
            if tok == "" or tok == "\n":
                continue
            else:
                self.tokens.append(tok)
        self.curr_tok_num = -1
    
    def hasMoreTokens(self):
        if not self.curr_tok_num == (len(self.tokens) -1):
            return True
        else:
            return False

    def advance(self):
        if self.hasMoreTokens():
            self.curr_tok_num += 1
            return (self.tokenType(),self.tokens[self.curr_tok_num])
        else:
            return (T_ERROR,None)
    
    def peek(self):
        if self.hasMoreTokens():
            peek_tok = self.tokens[self.curr_tok_num+1]
            peek_toktype = T_ERROR
            if peek_tok in keywords:
                peek_toktype =  T_KEYWORD
            elif peek_tok.isdigit():
                peek_toktype = T_NUM
            elif peek_tok[0] == "\"" or peek_tok[0] == "\'":
                peek_toktype = T_STR
            elif peek_tok in symbols:
                peek_toktype = T_SYM
            else:
                peek_toktype = T_ID
            return (peek_toktype, peek_tok)
        else:
            return (T_ERROR,None)
    
    def tokenType(self):
        curr_token = self.tokens[self.curr_tok_num]
        if curr_token in keywords:
            return T_KEYWORD
        elif curr_token.isdigit():
            return T_NUM
        elif curr_token[0] == "\"" or curr_token[0] == "\'":
            return T_STR
        elif curr_token in symbols:
            return T_SYM
        else:
            return T_ID
    
    def keyWord(self):
        curr_token = self.tokens[self.curr_tok_num]
        return keywords.index(curr_token)

    def symbol(self):
        return self.tokens[self.curr_tok_num]
    
    def identifier(self):
        return self.tokens[self.curr_tok_num]
    
    def intVal(self):
        return int(self.tokens[self.curr_tok_num])
    
    def stringVal(self):
        return self.tokens[self.curr_tok_num][1:-1]

