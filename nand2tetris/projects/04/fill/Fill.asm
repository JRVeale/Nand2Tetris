// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(MAIN)
	@KBD			//Check for keyboard input
	D=M																						
	@ON																						
	D;JNE				//If keyboard input go to ON										

	(OFF)	
		@onoff																					
		M=0					//0000000000000000													
		@UPDATE																					
		0;JMP				//Else do OFF only													
		
	(ON)
		@onoff																					
		M=-1				//1111111111111111													
		
	(UPDATE)
		@SCREEN																					
		D=A	
		@index
		M=D					//Set index to start of screen
		
		(LOOP)	
			@onoff
			D=M
			
			@index
			A=M					//Set register to index (current part of screen)
			
			M=D					//Set current part of screen as determined by keyboard at start
			
			@SCREEN																			
			D=A																						
			@8191																					
			D=D+A				//Last row of screen												
			
			@index																					
			M=M+1				//Update index for next screen register
			
			D=D-M
			@LOOP
		D;JGE				//If this wasn't last register on screen, keep updating screen
	@MAIN
	0;JMP				//Else, start over, checking for keyboard input
	
(END)
	@END
	0;JMP				//In case bad code causes escape...