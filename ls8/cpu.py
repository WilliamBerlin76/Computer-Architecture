"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Create branchtable
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[MUL] = self.handle_mul

        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
    def load(self, filename):
        """Load a program into memory."""

        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    
                    if num == '':
                        continue
                    
                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1
        # # For now, we've just hardcoded a program:
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
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
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def handle_prn(self, *argv):
        print(self.reg[argv[0]])
        self.pc += 2

    def handle_ldi(self, *argv):
        self.reg[argv[0]] = argv[1]
        self.pc += 3

    def handle_hlt(self, *argv):
        sys.exit(1)

    def handle_mul(self, *argv):
        self.alu('MUL', argv[0], argv[1])
        self.pc += 3
        
    def run(self):
        """Run the CPU."""
        
        running = True

        while running:
            
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1) 
            operand_b = self.ram_read(self.pc + 2)
            
            if instruction in self.branchtable:
                self.branchtable[instruction](operand_a, operand_b)
            else:
                print('did not understand the instruction')
                sys.exit(1)

