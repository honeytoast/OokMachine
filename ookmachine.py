#### Grace Hadiyanto
#### "ookmachine.py"
#### CS439

import sys

class OokMachine:
    __slots__ = {'_memory', '_data_ptr', '_inverse_lookup', '_lookup', 
                 '_program', '_instruction_ptr', '_instructions'}
    def __init__(self, filename):
        self._instructions = []
        self._instruction_ptr = 0
        self._memory = [0]
        self._data_ptr = 0
        # lookup table for returning a loop end index to its matching loop begin
        # index
        self._lookup = dict()

        # parse pairs of tokens from the program file to form a list of command 
        # instructions
        with open(filename, 'r') as self._program:
            for line in self._program:
                tokens = line.split()
                i = 0
                token_amount = len(tokens)
                while (i < token_amount):
                    command_token = tokens[i] + ' ' + tokens[i+1]
                    self._instructions.append(command_token)
                    i += 2
        
        # parse through the commands and keep track of beginning loop command
        # tokens on a stack. once an end loop command token is seen,
        # start popping the indexes of the beginning loop tokens from the stack.
        # each popped index will correspond to the correct end loop token index
        # and be added to a lookup table (dictionary).
        loop_start_index_stack = []
        for command_index, command in enumerate(self._instructions):
            if command == 'Ook! Ook?':
                loop_start_index_stack.append(command_index)
            elif command == 'Ook? Ook!':
                loop_begin_index = loop_start_index_stack.pop()
                self._lookup.update({loop_begin_index : command_index})

        # create the inverse lookup table used for returning a loop begin 
        # index to its matching loop end index.
        self._inverse_lookup = { end_loop_index : begin_loop_index for
                                 begin_loop_index, end_loop_index in 
                                 self._lookup.items() }

    def execute(self):
        """Executes the Ook Machine until its instruction pointer goes past the
        last command in its program."""
        endprogram = len(self._instructions)
        
        # create a mapping used to map a command token to its corresponding
        # function.
        command_map = { 'Ook. Ook?' : self.command1,
                        'Ook? Ook.' : self.command2,
                        'Ook. Ook.' : self.command3,
                        'Ook! Ook!' : self.command4,
                        'Ook! Ook.' : self.command5,
                        'Ook. Ook!' : self.command6,
                        'Ook! Ook?' : self.command7,
                        'Ook? Ook!' : self.command8 }
        while self._instruction_ptr < endprogram:        
            command_map[self._instructions[self._instruction_ptr]]()

    def command1(self):
        """Called when the command token is 'Ook. Ook?' - increments the data
        pointer."""
        # grow the current memory size to fit the needs of the machine.
        if self._data_ptr + 1 > len(self._memory) - 1:
            while self._data_ptr + 1 > len(self._memory) - 1:
                self._memory.append(0)
        self._data_ptr += 1
        self._instruction_ptr += 1

    def command2(self):
        """Called when the comand token is 'Ook? Ook.' - decrements the data
        pointer."""
        self._data_ptr -= 1
        self._instruction_ptr += 1

    def command3(self):
        """Called when the command token is 'Ook. Ook.' - increments the current
        byte."""
        self._memory[self._data_ptr] += 1
        self._instruction_ptr += 1

    def command4(self):
        """Called when the command token is 'Ook! Ook!' - decrements the current
        byte."""
        self._memory[self._data_ptr] -= 1
        self._instruction_ptr += 1

    def command5(self):
        """Called when the command token is 'Ook! Ook.' - writes the current
        byte to stdout."""
        print(chr(self._memory[self._data_ptr]), end='')
        self._instruction_ptr += 1

    def command6(self):
        """Called when the command token is 'Ook. Ook!.' - reads a character from
        stdin and overwrites the current byte with it."""
        self._memory[self._data_ptr] = ord(input('\n> '))
        self._instruction_ptr += 1

    def command7(self):
        """Called when the command token is 'Ook! Ook?' - start of a loop,
        if the current byte is 0 do nothing and go to the next instruction,
        else, jump to the end of the corresponding 'Ook? Ook!'"""
        if self._memory[self._data_ptr] != 0:
            self._instruction_ptr += 1
        else:
            # look up the corresponding loop end index for the begin loop and
            # add by 1 to set the instruction ptr past it.
            self._instruction_ptr = self._lookup[self._instruction_ptr] + 1

    def command8(self):
        """Called when the command token is 'Ook? Ook!' - end of a loop,
        jump back to the corresponding 'Ook! Ook?'"""
        self._instruction_ptr = self._inverse_lookup[self._instruction_ptr]

    # Ook! machine's memory string reperesentation for debugging purposes
    def __repr__(self):
        return str(self._memory)

def main():
    if len(sys.argv) != 2:
        print('Error, usage: python3 ookmachine.py <filename>')
        print('Where <filename> is the name of a .ook file')
        exit()
    filename = sys.argv[1]
    ook_machine = OokMachine(filename)
    ook_machine.execute()

if __name__ == '__main__':
    main()
