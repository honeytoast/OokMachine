# OokMachine
A project for Theory of Computability class that emulates the execution of a turing tarpit, Ook!, Machine

Included files: triangle.ook  -  Ook! program that prints out the Serpinski triangle
ookmachine.py -  Python3 source code that emulates an Ook! machine

How to run:
python3 ookmachine.py <name of .ook file>

About the project:

The Ook! language is a Turing tarpit, a model of an algorithm that is minimalist and/or humorous, and also barely Turing-complete.

This program will emulate an Ook! machine which is defined by:
1. A memory - an array of bytes, principally unbounded, like the length of a Turing tape
2. A data pointer - that holds the address of one byte
3. stdin and stdout - which can be read or written one character at a time
4. A program - a set of valid Ook! instructions stored in a text format. The memory and program are stored separately.
5. An instruction pointer - holding the index of the current command within the program.

The current byte is the contents of the memory at the current value of the data pointer.

An Ook! program is stored in an ASCII text file and is made up of three tokens separated by whitespace: "Ook.", "Ook!", and "Ook?". Two consecutive tokens separated by whitespace form a command. There are 8 commands:
1. Ook. Ook?   -     Increments the data pointer
2. Ook? Ook.   -     Decrements the data pointer
3. Ook. Ook.   -     Increments the current byte
4. Ook! Ook!   -     Decrements the current byte
5. Ook! Ook.   -     Write the current byte to stdout
6. Ook. Ook!   -     Reads a character from stdin and overwrites the current byte with it
7. Ook! Ook?   -     Begins a loop; if the current byte is zero, do nothing. Else, jump past the matching Ook? Ook!
8. Ook? Ook!   -     End of a loop; jump back to the matching Ook! Ook?

Initially every memory byte, data pointer, and instruction pointer are set to 0. An Ook! machine decides the meaning of the command at the current instruction pointer, executes it, and adjusts the instruction pointer accordingly to the command that was executed. After commands 1-6, the instruction pointer is incremented by 1 so that it points to the next command. Commands 7 and 8 correspond to a while loop. The program terminates when the instruction pointer goes past the last command.
