class Assembler:

    def assemble(self,filepath):
        lines = self.loadasm(filepath)
        barelines = self.removewhitespace(lines)
        binarylines = self.translate(barelines)
        self.savehack(binarylines,filepath)


    def loadasm(self,filepath):
        f = open(filepath,"r")
        lines = f.readlines()
        f.close()
        return lines

    def savehack(self,hacklines,asmfilepath):
        hackfilepath = asmfilepath[:-3] + "hack"
        f = open(hackfilepath,"w+")
        f.writelines(hacklines)
        f.close()

    def removewhitespace(self,rawasm):
        cleanlines = []
        for line in rawasm:
            stripped = line.strip()
            nocomment = self.removecomments(stripped,"//").strip()
            if nocomment != "":
                cleanlines.append(nocomment)
        return cleanlines

    def removecomments(self,line,commentstr):
        if commentstr in line:
            return line[:line.index(commentstr)]
        else:
            return line

    def translate(self,asmlines):
        binarylines = []
        for line in asmlines:
            if "@" in line:
                #a-instruction
                binarylines.append(self.ainstrtobinary(line) + "\n")
            else:
                #c-instruction
                binarylines.append(self.cinstrtobinary(line) + "\n")
        return binarylines

    def ainstrtobinary(self,asm):
        address = str(bin(int(asm[1:])))[2:]
        assert (len(address) < 16), "address too large in: " + asm + " " + address
        padlength = 16 - len(address)
        padding = "0"*padlength
        binaryline = padding + address
        assert (len(binaryline) == 16), "bad translation of: " + asm
        return binaryline

    def cinstrtobinary(self,asm):
        comp, dest, jump = self.splitcinstr(asm)
        c = self.getcompbin(comp)
        assert (len(c) == 7), "bad c"
        d = self.getdestbin(dest)
        assert (len(d) == 3), "bad d"
        j = self.getjumpbin(jump)
        assert (len(j) == 3), "bad j"
        instruction = c + d + j
        binaryline = "111" + instruction
        assert (len(binaryline) == 16), "bad translation of: " + asm
        return binaryline

    def splitcinstr(self,asm):
        comp = asm
        dest = ""
        jump = ""
        if "=" in comp:
            index = comp.index("=")
            dest = comp[:index]
            comp = comp[index+1:]
        if ";" in comp:
            index = comp.index(";")
            jump = comp[index+1:]
            comp = comp[:index]
        return comp,dest,jump

    def getcompbin(self,comp):
        a=c1=c2=c3=c4=c5=c6="0"
        if "M" in comp:
            a = "1"

        if comp == "0":
            c1=c3=c5="1"
        elif comp == "1":
            c1=c2=c3=c4=c5=c6="1"
        elif comp == "-1":
            c1=c2=c3=c5="1"
        elif comp == "D":
            c3=c4="1"
        elif comp == "A" or comp == "M":
            c1=c2="1"
        elif comp == "!D":
            c3=c4=c6="1"
        elif comp == "!A" or comp == "!M":
            c1=c2=c6="1"
        elif comp == "-D":
            c3=c4=c5=c6="1"
        elif comp == "-A" or comp == "-M":
            c1=c2=c5=c5="1"
        elif comp == "D+1":
            c2=c3=c4=c5=c6="1"
        elif comp == "A+1" or comp == "M+1":
            c1=c2=c4=c5=c6="1"
        elif comp == "D-1":
            c3=c4=c5="1"
        elif comp == "A-1" or comp == "M-1":
            c1=c2=c5="1"
        elif comp == "D+A" or comp == "D+M":
            c5="1"
        elif comp == "D-A" or comp == "D-M":
            c2=c5=c6="1"
        elif comp == "A-D" or comp == "M-D":
            c4=c5=c6="1"
        elif comp == "D&A" or comp == "D&M":
            None
        elif comp == "D|A" or comp == "D|M":
            c2=c4=c6="1"

        return a + c1 + c2 + c3 + c4 + c5 + c6

    def getdestbin(self,dest):
        if dest == "":
            return "000"
        else:
            d1 = d2 = d3 = "0"
            if "M" in dest:
                d3 = "1"
            if "D" in dest:
                d2 = "1"
            if "A" in dest:
                d1 = "1"
            return d1+d2+d3

    def getjumpbin(self,jump):
        if jump == "":
            return "000"
        elif jump == "JMP":
            return "111"
        else:
            j1 = j2 = j3 = "0"
            if "G" in jump:
                j3 = "1"
            elif "L" in jump:
                j1 = "1"
            if "NE" in jump:
                j1 = "1"
                j3 = "1"
            elif "E" in jump:
                j2 = "1"
            return j1+j2+j3



a = Assembler()
a.assemble(r"C:\Users\James\Documents\GitHub\Nand2Tetris\nand2tetris\projects\06\add\Add.asm")
a.assemble(r"C:\Users\James\Documents\GitHub\Nand2Tetris\nand2tetris\projects\06\max\MaxL.asm")
a.assemble(r"C:\Users\James\Documents\GitHub\Nand2Tetris\nand2tetris\projects\06\rect\RectL.asm")
a.assemble(r"C:\Users\James\Documents\GitHub\Nand2Tetris\nand2tetris\projects\06\pong\PongL.asm")