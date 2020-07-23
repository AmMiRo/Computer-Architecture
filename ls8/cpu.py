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
        # reg[7] acts as a stack pointer
        self.reg[7] = 0xF4
        # flag used for ><= operations
        self.fl = 0
        # dispatch/branch table
        self.dispatch_table = {
            # ALU operations
            0b10100000: "ADD",
            0b10100001: "SUB",
            0b10100010: "MUL",
            0b10100011: "DIV",
            0b10100100: "MOD",
            0b01100101: "INC",
            0b01100110: "DEC",
            0b10100111: "CMP",
            0b10101000: "AND",
            0b01101001: "NOT",
            0b10101010: "OR",
            0b10101011: "XOR",
            0b10101100: "SHL",
            0b10101101: "SHR",
            
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
        elif op == "DIV":
            if self.reg[reg_b] == 0:
                print("You cannot devide by 0")
                exit()
            else:
                self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "CMP":
            val_1 = self.reg[self.ram_read(self.pc + 1)]
            val_2 = self.reg[self.ram_read(self.pc + 2)]
            if val_1 == val_2:
                self.fl = 0b001
            elif val_1 < val_2:
                self.fl = 0b100
            elif val_1 > val_2:
                self.fl = 0b010
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        # print(f"TRACE: %02X | %02X %02X %02X |" % (
        #     self.pc,
        #     # self.fl,
        #     #self.ie,
        #     self.ram_read(self.pc),
        #     self.ram_read(self.pc + 1),
        #     self.ram_read(self.pc + 2)
        # ), end='')

        print(self.pc)

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # initialize instruction register as 0
        ir = 0
        # while loop ends at HLT (0b00000001 = 1)
        while ir != 1:
            # self.trace()
            # set ir to the first instruction in ram
            ir = self.ram_read(self.pc)
            # if ir is ALU operation pass to call ALU function
            if (ir >> 5) & 0b001 == 1:
                self.alu(self.dispatch_table[self.ram_read(self.pc)], self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            # if ir is NOP
            elif ir == 0:
                continue
            # if ir is LDI (0b10000010 = 130)
            elif ir == 130:
                # set reg at address LDI + 1 equal to value at LDI + 2
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
            # if ir is LD
            elif ir == 131:
                # reg at address LD + 1 equal to value at ram[address stored in register b]
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.reg[self.ram_read(self.pc + 2)])
            # if ir is ST
            elif ir == 132:
                # store value in reg_b in address in reg_a
                self.ram_write(self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            # if ir is PUSH
            elif ir == 69:
                # decrement sp and place value from pc + 1 in address sp
                self.reg[7] -= 1
                self.ram_write(self.reg[7], self.reg[self.ram_read(self.pc + 1)])
            # if ir is POP
            elif ir == 70:
                # place value from address ps to register at pc + 1
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.reg[7])
                self.reg[7] += 1
            # elif ir is PRN (0b01000111 = 71)
            elif ir == 71:
                # print value at reg at address PRN + 1
                print(self.reg[self.ram_read(self.pc + 1)])
            # if ir is PRA ????????????????????????????????????????????????????????????
            elif ir == 72:
                pass
            # check if ir mutates the pc
            if (ir >> 4) & 0b0001 == 0:
                # incriment program counter by 1 and number of operands
                self.pc += 1 + (ir >> 6)
            elif (ir >> 4) & 0b0001 == 1:
                # if ir is CALL
                if ir == 80:
                    self.reg[7] -= 1
                    self.ram_write(self.reg[7], self.pc + 2)
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                # if ir is RET
                if ir == 17:
                    self.pc = self.ram_read(self.reg[7])
                    self.reg[7] += 1
                # if ir is INT
                if ir == 82:
                    pass
                # if ir is IRET
                if ir == 19:
                    pass
                # if ir is JMP
                if ir == 84:
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                # if ir is JEQ
                if ir == 85:
                    if self.fl & 0b001 == 1:
                        self.pc = self.reg[self.ram_read(self.pc + 1)]
                    else:
                        self.pc += 2
                # if ir is JNE
                if ir == 86:
                    if self.fl & 0b001 == 0:
                        self.pc = self.reg[self.ram_read(self.pc + 1)]
                    else:
                        self.pc += 2
                # if ir is JGT
                if ir == 87:
                    pass
                # if ir is JLT
                if ir == 88:
                    pass
                # if ir is JLE
                if ir == 89:
                    pass
                # if ir is JGE
                if ir == 90:
                    pass

