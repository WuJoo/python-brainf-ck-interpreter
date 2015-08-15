import sys
import readchar


"""
Python Brainfuck interpreter
author Wiktor Jeziorski

TODO:
osluga kodu z plikow

examples:

$ python brainfuck.py
Python Brainfuck Interpreter
>++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.
Hello World!

"""


class IllegalCommandError(ValueError):
    def __init__(self, message):
        super(IllegalCommandError, self).__init__(message)


class BrainfuckInterpreter(object):
    def __init__(self, mem_len=30000):
        self.MEMORY_LENGTH = mem_len
        self.MEMORY = [0 for _ in xrange(self.MEMORY_LENGTH)]
        self.memory_pointer = 0
        self.command_pointer = None
        self.command = None
        self.right_parenthesis = None
        self.left_parenthesis = None

    def execute(self, command):
        self.command = command
        self.command_pointer = 0
        BrainfuckInterpreter.__get_parenthesis(self, command)
        while self.command_pointer < len(self.command):
            symbol = self.command[self.command_pointer]
            if symbol in '[]':
                if symbol == '[':
                    BrainfuckInterpreter.__left_parenthesis(self)
                elif symbol == ']':
                    BrainfuckInterpreter.__right_parenthesis(self)
            elif symbol in '><+-.,':
                if symbol == '>':
                    BrainfuckInterpreter.__move_right(self)
                elif symbol == '<':
                    BrainfuckInterpreter.__move_left(self)
                elif symbol == '+':
                    BrainfuckInterpreter.__increase(self)
                elif symbol == '-':
                    BrainfuckInterpreter.__decrease(self)
                elif symbol == '.':
                    BrainfuckInterpreter.__print_ascii(self)
                elif symbol == ',':
                    BrainfuckInterpreter.__get_ascii(self)
                self.command_pointer += 1
            else:
                self.command_pointer += 1

    def __move_right(self):
        self.memory_pointer += 1
        if self.memory_pointer == self.MEMORY_LENGTH:
            self.memory_pointer = 0

    def __move_left(self):
        self.memory_pointer -= 1
        if self.memory_pointer == -1:
            self.memory_pointer = self.MEMORY_LENGTH - 1

    def __increase(self):
        self.MEMORY[self.memory_pointer] += 1

    def __decrease(self):
        self.MEMORY[self.memory_pointer] -= 1

    def __print_ascii(self):
        sys.stdout.write(chr(self.MEMORY[self.memory_pointer]))

    def __get_ascii(self):
        ch = readchar.readchar()
        self.MEMORY[self.memory_pointer] = ord(ch)

    def __left_parenthesis(self):
        if self.MEMORY[self.memory_pointer] == 0:
            self.command_pointer = self.right_parenthesis[self.command_pointer]+1
        else:
            self.command_pointer += 1

    def __right_parenthesis(self):
        self.command_pointer = self.left_parenthesis[self.command_pointer]

    def __get_parenthesis(self, command):
        self.right_parenthesis = dict()
        self.left_parenthesis = dict()

        stack = []

        for i, symbol in enumerate(command):
            if symbol == '[':
                stack.append(i)
            elif symbol == ']':
                if stack:
                    left_par = stack.pop()
                    self.right_parenthesis[left_par] = i
                    self.left_parenthesis[i] = left_par
                else:
                    raise IllegalCommandError('Incorrect command line!')

        if stack:
            raise IllegalCommandError('Incorrect command line!')


def main():
    bf = BrainfuckInterpreter()
    print 'Python Brainfuck Interpreter'
    while True:
        command = raw_input('>')
        try:
            bf.execute(command)
        except IllegalCommandError as e:
            print e.message


if __name__ == "__main__":
    main()