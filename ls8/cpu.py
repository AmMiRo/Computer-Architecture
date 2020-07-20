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

    #function to return value at address in memory (see mar in ls8-spec)
    def ram_read(self, mar):
        return self.ram[mar]
        
    # function to write value to address in ram
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
            # if ir is LDI (0b10000010 = 130)
            if ir == 130:
                # set reg at address LDI + 1 equal to value at LDI + 2
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 3
            # elif ir is PRN (0b01000111 = 71)
            elif ir == 71:
                # print value at reg at address PRN + 1
                print(self.reg[self.ram_read(self.pc + 1)])
                self.pc += 2


