// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R2			//Set A to RAM2
	M=0			//Set RAM2 (the RAM pointed to by A) to 0
	
(LOOP)			//Multiply is +R1, R0 times.

	@R0			//Set A to RAM0
	D=M			//Set D to value of RAM0
	
	@END
	D;JLE		//if D (value in RAM0) <= 0, GOTO END (address in A)

	@R1			//Set A to RAM1
	D=M			//Set D to value of RAM0

	@R2			//Set A to RAM2
	M=M+D		//Add D (value of RAM1) to M (RAM2)
	@R0			//Set A to RAM0
	M=M-1		//Decrement value in RAM0
	
	@LOOP		//Set A to LOOP.
	0;JMP		//GOTO LOOP (address in A)
	
(END)
	@END		//Set A to END.
	0;JMP		//goto END (address in A)
	
	