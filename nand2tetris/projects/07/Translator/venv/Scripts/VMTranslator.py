# Nand2Tetris Week 7

# Develop a VM Translator (from Hack's VM to Hack Assembly)
## I'll bother to use the suggested design this time.

from enum import Enum

class CommandType(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9

class Parser:

    def __init__(self, pathin):
        fin = open(pathin,"r")
        self.lines = fin.readlines()
        self.currentline = 0
        fin.close()

    def hasMoreCommands(self):
        return self.currentline < len(self.lines)

    def lineNotCode(self):
        isblank = self.lines[self.currentline].strip() == ""
        isnotcode = self.lines[self.currentline].strip().startswith("//")
        return isblank or isnotcode
    def advance(self):
        self.currentline += 1
        if self.hasMoreCommands():
            if self.lineNotCode():
                self.advance()

    def commandType(self):
        line = self.lines[self.currentline].strip()

        if line.split()[0] == "push":
            return CommandType.C_PUSH

        if line.split()[0] == "pop":
            return CommandType.C_POP

        arithmetics = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or",
                       "not"]
        if line in arithmetics:
            return CommandType.C_ARITHMETIC

    def isArithmetic(self):
        return self.commandType() == CommandType.C_ARITHMETIC

    def isPushPop(self):
        ispush = self.commandType() == CommandType.C_PUSH
        ispop = self.commandType() == CommandType.C_POP
        return ispush or ispop

    def getCmdArg(self,argnum):
        arg = self.lines[self.currentline].strip().split()[argnum]
        return arg

    def arg1(self):
        if self.isArithmetic():
            return self.getCmdArg(0)
        return self.getCmdArg(1)

    def arg2(self):
        return self.getCmdArg(2)

    def line(self):
        return self.lines[self.currentline]


class CodeWriter:

    def __init__(self, pathout):
        self.fout = open(pathout, "w+")

    def a_instr(self, valuestr):
        return "@" + valuestr + "\n"

    def incrM(self):
        return "M=M+1\n"

    def pushDtostack(self):
        return self.a_instr("SP") + "A=M\nM=D\n" + self.a_instr("SP") + self.incrM() + "\n"

    def popstackto(self, dest, comp):
        return self.a_instr("SP") + "AM=M-1\n" + dest + "=" + comp + "\n\n"

    def writeComment(self, comment):
        self.fout.write(r"// " + comment)

    def writeArithmetic(self, operation):

        hackstring = ""

        if operation == "add":
            #pop to D, pop and add to D, push D
            hackstring += self.popstackto("D","M")
            hackstring += self.popstackto("D","D+M")
            hackstring += self.pushDtostack()

        #TODO

        self.fout.write(hackstring)

    def writePushPop(self, command, segment, index):

        hackstring = ""

        if command == CommandType.C_PUSH:

            if segment == "constant":

                hackstring += self.a_instr(index) + "D=A\n\n"

            hackstring += self.pushDtostack()

        self.fout.write(hackstring)

    def close(self):
        self.fout.close()

def translateVM(path):

    parser = Parser(path)
    pathout = path[:-2] + "asm"
    writer = CodeWriter(pathout)

    while parser.hasMoreCommands():

        if not parser.lineNotCode():
            writer.writeComment(parser.line())

        if parser.isArithmetic():
            writer.writeArithmetic(parser.arg1())

        elif parser.isPushPop():
            writer.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())

        parser.advance()

    writer.close()