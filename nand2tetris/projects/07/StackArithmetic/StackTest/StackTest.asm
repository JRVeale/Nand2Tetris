// push constant 17
@17
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A

@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL0
D,JEQ
D=0
@ENDBOOL0
0,JMP
(BOOL0)
D=-1
(ENDBOOL0)

@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 16
@16
D=A

@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL1
D,JEQ
D=0
@ENDBOOL1
0,JMP
(BOOL1)
D=-1
(ENDBOOL1)

@SP
A=M
M=D
@SP
M=M+1

// push constant 16
@16
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A

@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL2
D,JEQ
D=0
@ENDBOOL2
0,JMP
(BOOL2)
D=-1
(ENDBOOL2)

@SP
A=M
M=D
@SP
M=M+1

// push constant 892
@892
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A

@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL3
D,JLT
D=0
@ENDBOOL3
0,JMP
(BOOL3)
D=-1
(ENDBOOL3)

@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 892
@892
D=A

@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL4
D,JLT
D=0
@ENDBOOL4
0,JMP
(BOOL4)
D=-1
(ENDBOOL4)

@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A

@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL5
D,JLT
D=0
@ENDBOOL5
0,JMP
(BOOL5)
D=-1
(ENDBOOL5)

@SP
A=M
M=D
@SP
M=M+1

// push constant 32767
@32767
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A

@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL6
D,JGT
D=0
@ENDBOOL6
0,JMP
(BOOL6)
D=-1
(ENDBOOL6)

@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 32767
@32767
D=A

@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL7
D,JGT
D=0
@ENDBOOL7
0,JMP
(BOOL7)
D=-1
(ENDBOOL7)

@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A

@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@BOOL8
D,JGT
D=0
@ENDBOOL8
0,JMP
(BOOL8)
D=-1
(ENDBOOL8)

@SP
A=M
M=D
@SP
M=M+1

// push constant 57
@57
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 31
@31
D=A

@SP
A=M
M=D
@SP
M=M+1

// push constant 53
@53
D=A

@SP
A=M
M=D
@SP
M=M+1

// add
@SP
AM=M-1
D=M

@SP
AM=M-1
D=D+M

@SP
A=M
M=D
@SP
M=M+1

// push constant 112
@112
D=A

@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M

@SP
AM=M-1
D=M-D

@SP
A=M
M=D
@SP
M=M+1

// neg
@SP
A=M-1
M=-M// and
@SP
AM=M-1
D=M

@SP
AM=M-1
D=D&M

@SP
A=M
M=D
@SP
M=M+1

// push constant 82
@82
D=A

@SP
A=M
M=D
@SP
M=M+1

// or
@SP
AM=M-1
D=M

@SP
AM=M-1
D=D|M

@SP
A=M
M=D
@SP
M=M+1

// not
@SP
A=M-1
M=!M