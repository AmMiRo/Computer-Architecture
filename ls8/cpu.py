"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # initialize program counter as 0
        self.pc = 0
        # initialize ram (memory for instructions) w/ 256 * 0s
        self.ram = [0] * 256
        # initialize register with 8 * 0s
        self.reg = [0] * 8
        # dispatch/branch table
        self.dispatch_table = {
            # ALU operations
            0b10100000: "ADD",
            0b10100001: "SUB",
            0b10100010: "MUL"
        }

    #function to return value at address in memory (see mar in ls8-spec)
    def ram_read(self, mar):
        return self.ram[mar]
        
    # function to write value to address in ram
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, file):
        """Load a program into memory."""
        address = 0

        try:
            with open(file) as program:
                for line in program:
                    command = line.split("#")[0].strip()
                    if command == "":
                        continue
                    num = int(command, 2)
                    self.ram_write(address, num)
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # initialize instruction register as 0
        ir = 0
        # while loop ends at HLT (0b00000001 = 1)
        while ir != 1:
            # set ir to the first instruction in ram
            ir = self.ram_read(self.pc)
            # if ir is ALU operation pass to call ALU function
            if (ir >> 5) & 0b001 == 1:
                self.alu(self.dispatch_table[self.ram[self.pc]], self.ram[self.pc + 1], self.ram[self.pc + 2])
            # if ir is LDI (0b10000010 = 130)
            if ir == 130:
                # set reg at address LDI + 1 equal to value at LDI + 2
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
            # elif ir is PRN (0b01000111 = 71)
            elif ir == 71:
                # print value at reg at address PRN + 1
                print(self.reg[self.ram_read(self.pc + 1)])
            # incriment program counter by 1 and number of operands
            # self.trace()
            self.pc += 1 + (ir >> 6)

