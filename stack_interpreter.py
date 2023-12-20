import sys


class Stack:
    """Class that represents a stack and its commands"""
    def __init__(self, size):
        self.buffer = [0 for _ in range(size)]
        self.s_pointer = -1

    def push(self, number):
        """Adds value to the stack"""
        self.s_pointer += 1
        self.buffer[self.s_pointer] = number

    def pop(self):
        """Removes value from stack"""
        number = self.buffer[self.s_pointer]
        self.s_pointer -= 1
        return number

    def top(self):
        """Returns the top of the stack"""
        return self.buffer[self.s_pointer]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: python stack_interpreter.py filename")
        exit(1)
    file_name = sys.argv[1]  # reads file name from command line argument
    with open(file_name, "r") as read_file:
        file_lines = [line.strip() for line in read_file.readlines()]  # Separates lines and removes whitespace
    program = []
    token_counter = 0
    label_tracker = {}

    for line in file_lines:
        parts = line.split(" ")
        cmd = parts[0]  # prepares the first command
        if cmd == "":
            # checks if current cmd is empty
            continue
        if cmd.endswith(":"):
            # checks if cmd is a valid label
            label_tracker[cmd[:-1]] = token_counter
            continue
        program.append(cmd)  # stores cmd token
        token_counter += 1
        # executes each command
        if cmd == "PUSH":
            num = int(parts[1])
            program.append(num)  # adds value to the stack
            token_counter += 1
        elif cmd == "PRINT":
            # handles command to print out string
            print_str = ' '.join(parts[1:])
            program.append(print_str)
            token_counter += 1
        elif cmd == "JUMP.EQUAL.0":
            label = parts[1]
            program.append(label)
            token_counter += 1
        elif cmd == "JUMP.GET.0":
            label = parts[1]
            program.append(label)
            token_counter += 1

    p_cmd = 0
    prog_stack = Stack(256)  # creates the stack to run each command

    while program[p_cmd] != "STOP":
        cmd = program[p_cmd]
        p_cmd += 1
        if cmd == "PUSH":
            num = program[p_cmd]
            p_cmd += 1
            prog_stack.push(num)
        elif cmd == "POP":
            prog_stack.pop()
        elif cmd == "ADD":
            # handles adding values
            a = prog_stack.pop()  # grabs the first value
            b = prog_stack.pop()  # grabs the second value
            prog_stack.push(a + b)  # adds the sum of a and b to the stack
        elif cmd == "SUB":
            a = prog_stack.pop()
            b = prog_stack.pop()
            prog_stack.push(b - a)  # adds the difference of a and b to the stack
        elif cmd == "PRINT":
            print_str = program[p_cmd]
            p_cmd += 1
            print(print_str)
        elif cmd == "READ":
            num = int(input())
            prog_stack.push(num)
        elif cmd == "JUMP.EQUAL.0":
            num = prog_stack.top()
            if num == 0:
                p_cmd = label_tracker[program[p_cmd]]
            else:
                p_cmd += 1
        elif cmd == "JUMP.GET.0":
            num = prog_stack.top()
            if num > 0:
                p_cmd = label_tracker[program[p_cmd]]
            else:
                p_cmd += 1
        else:
            print("Invalid command")
            exit(0)
