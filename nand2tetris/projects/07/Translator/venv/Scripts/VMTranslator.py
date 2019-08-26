# Nand2Tetris Week 7

# Develop a VM Translator (from Hack's VM to Hack Assembly)
## I'll bother to use the suggested design this time.

from enum import Enum
import os

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

class CodeWriterLookupError(LookupError):
    '''raise this when no translation available'''

class ParsingError(ValueError):
    '''raise this when bad VM Code provided'''

class CodeWriter:

    def __init__(self, pathout):
        self.fout = open(pathout, "w+")
        self.boolcount = 0
        self.filename = os.path.split(pathout)[1][:-3]

    def a_instr(self, valuestr):
        return "@" + valuestr + "\n"

    def incrM(self):
        return "M=M+1\n"

    def inplacestackop(self, operation):
        if operation == "not":
            temp = "!"
        elif operation == "neg":
            temp = "-"
        else:
            raise CodeWriterLookupError("Bad in place stack operator - " + operation)
        return self.a_instr("SP")+"A=M-1\nM=" + temp + "M"

    def pushDtostack(self):
        return self.a_instr("SP") + "A=M\nM=D\n" + self.a_instr("SP") + self.incrM() + "\n"

    def popstackto(self, dest, comp):
        return self.a_instr("SP") + "AM=M-1\n" + dest + "=" + comp + "\n\n"

    def popstacktoD(self):
        return self.popstackto("D","M")

    def boolcompareD(self, jump):
        label = "BOOL" + str(self.boolcount)
        endlabel = "END" + label
        temp = self.a_instr(label) + "D," + jump + "\nD=0\n" \
               +  self.a_instr(endlabel) + "0,JMP\n(" + label +")\nD=-1\n(" \
               +  endlabel + ")\n\n"
        return temp

    def writeComment(self, comment):
        self.fout.write(r"// " + comment)

    def writeArithmetic(self, operation):

        hackstring = ""

        if operation in ["neg", "not"]:
            # in-place
            hackstring += self.inplacestackop(operation)

        else:
            hackstring += self.popstackto("D", "M")

            if operation in ["eq","gt","lt"]:
                # boolean
                hackstring += self.popstackto("D", "M-D")
                if operation == "eq":
                    jump = "JEQ"
                elif operation == "gt":
                    jump = "JGT"
                elif operation == "lt":
                    jump = "JLT"
                else:
                    raise CodeWriterLookupError("Bad boolean operator! - " + operation)
                hackstring += self.boolcompareD(jump)
                self.boolcount += 1

            elif operation in ["add", "sub", "and", "or"]:
                #comp
                if operation == "add":
                    #pop to D, pop and add to D, push
                    comp = "D+M"

                elif operation == "sub":
                    # pop to D, subtract D from next pop, push
                    comp = "M-D"

                elif operation == "and":
                    # pop to D, AND D with next pop, push
                    comp = "D&M"

                elif operation == "or":
                    # pop to D, OR D with next pop, push D
                    comp = "D|M"

                hackstring += self.popstackto("D",comp)

            else:
                raise CodeWriterLookupError("Bad operator! - " + operation)

            hackstring += self.pushDtostack() + "\n"

        self.fout.write(hackstring)

    def writePushPop(self, command, segment, index):

        if command == CommandType.C_PUSH:

            self.fout.write(self.buildpush(segment, index))

        elif command == CommandType.C_POP:

            self.fout.write(self.buildpop(segment, index))

        else:
            raise CodeWriterLookupError("Incorrect command type for PushPop")

    def buildpush(self, segment, index):

        if segment == "constant":

            registerintoD = "A"

        else:

            registerintoD = "M"

        return self.putcorrectaddressinA(segment, index) + "D=" \
               + registerintoD + "\n\n" + self.pushDtostack() + "\n"

    def buildpop(self, segment, index):

        if segment == "constant":

            raise ParsingError("Cannot pop to constant segment!")

        address, reltobaseaddress = self.getaddress(segment, index)

        if reltobaseaddress:

            prefix = self.a_instr(address) + "D=M\n" + self.a_instr(index) \
                     + "D=D+A\n\n" + self.a_instr("R13") + "M+D\n\n"
            suffix = self.a_instr("R13") + "A=M\nM=D\n\n"

        else:

            prefix = ""
            suffix = self.a_instr(address) + "M=D\n\n"

        return prefix + self.popstacktoD() + suffix + "\n"

    def putcorrectaddressinA(self, segment, index):

        address, reltobaseaddress = self.getaddress(segment, index)

        if reltobaseaddress:

            suffix = "D=M\n" + self.a_instr(index) + "A=D+A\n\n"

        else:

            suffix = "\n"

        return self.a_instr(address) + suffix

    def getaddress(self, segment, index):

        reltobaseaddress = False

        if segment == "constant":

            address = index

        elif segment == "temp":

            address = str(int(index) + 5)

        elif segment == "pointer":

            if index == "0":

                address = "THIS"

            elif index == "1":

                address = "THAT"

            else:

                raise ParsingError("Attempted to access pointer " + index
                                   + ", must be 0 or 1")

        elif segment == "static":

            address = self.filename + index

        elif segment == "local":

            address = "LCL"
            reltobaseaddress = True

        elif segment == "argument":

            address = "ARG"
            reltobaseaddress = True

        elif segment == "this":

            address = "THIS"
            reltobaseaddress = True

        elif segment == "that":

            address = "THAT"
            reltobaseaddress = True

        else:

            raise ParsingError(segment + " segment was not recognised.")

        return address, reltobaseaddress

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