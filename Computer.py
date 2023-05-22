from itertools import product
import os

from Gates import Mux16
from Chips import Inc16, CPU
from Memory import Register, RAM64k


class Computer:
    # name = Computer
    # value = ?
    def __init__(self, prog):
        self.mem = RAM64k()  # M, Value = 9 437 184
        # input("RAM Made")
        self.program = prog  # ROM, Value = ?
        self.regA = Register()  # A, Value = 144
        self.regD = Register()  # D, Value = 144
        self.regPC = Register()  # PC, Value = 144
        # Other Value: 672 > 1104
        # - CPU: 548
        # - Mux16: 49
        # - Inc16: 75

    def clock(self):
        ROM_address = int(''.join(map(str, self.regPC.clock([0]*16, 0))), 2)  # TODO - Use binary saving
        if ROM_address > len(self.program) - 1:
            print('END OF PROGRAM')
            exit(0)
        regA_data = self.regA.clock([0]*16, 0)
        regD_data = self.regD.clock([0]*16, 0)
        mem_data = self.mem.clock([0]*16, regA_data, 0)
        [alu_out, save, jump] = CPU(self.program[ROM_address], regA_data, regD_data, mem_data)
        regA_data = self.regA.clock(alu_out, save[0])
        self.regD.clock(alu_out, save[1])
        self.mem.clock(alu_out, regA_data, save[2])
        PC = self.regPC.clock([0] * 16, 0)
        PC = Mux16(Inc16(PC), regA_data, jump)
        PC = self.regPC.clock(PC, 1)
        # input("Clock Successful")

    def print_top(self, decimal, amount):
        os.system('cls' if os.name == 'nt' else 'clear')
        inputs = ["".join(seq) for seq in product("01", repeat=amount)]
        print(f'Computer 2')
        print("Register A : " + str(self.regA.clock([0] * 16, 0)))
        print("Register D : " + str(self.regD.clock([0] * 16, 0)))
        print("Register PC : " + str(self.regPC.clock([0] * 16, 0)))
        for i in inputs:
            if decimal:
                print(str("% 2s" % int(i, 2)) + ": " + str(int(''.join(
                    map(str, self.mem.clock([0] * 16, [0] * (16 - amount) + [*map(int, list(i))], 0))), 2)))
            else:
                print(str("% 2s" % int(i, 2)) + ": " + str(
                    self.mem.clock([0] * 16, [0] * (16 - amount) + [*map(int, list(i))], 0)))
        input()


program = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],  # REG A = 21
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # A, SAV D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # REG A = 9
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]  # A+D, SAV M[A], NONE
]

program = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],  # 00 - A = 5
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 01 - A, D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 02 - A = 0
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # 03 -  D, M, NONE

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 04 - A = 1       >> @I
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0],  # 05 - 1, M, NONE  >> @I = 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 06 - A = 2       >> @S
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # 07 - 0, M, NONE  >> @S = 0
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 08 - A = 1       >> LOOP
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 09 - M, D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10 - A = 0
    [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],  # 11 - M-D, D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],  # 12 - A = 22     >> STOP location
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],  # 13 - D, NONE, JLT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 14 - A = 1
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 15 - M, D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 16 - A = 2
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # 17 - D+M, M, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 18 - A = 1
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0],  # 19 - M+1, M, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # 20 - A = 8       >> LOOP Location
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1],  # 21 - 0, NONE, JMP
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],  # 22 - A = 2       >> STOP
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]  # 23 - M, A, NONE
]


computer = Computer(program)  # Setup computer
while True:
    computer.clock()  # Run instruction
    computer.print_top(True, 2)  # Print changes, In decimal, 2^2 registers

# If a == 0 then X = D, Y = A
# If a == 1 then X = D, Y = M

# ALU Logic (C1-C6)
# Zx Nx Zy Ny F No = F(x,y) [a=0], [a=1]
# 101010 = 0, Null
# 111111 = 1, Null
# 111010 = -1, Null
# 001100 = D
# 110000 = A, M
# 001101 = !D
# 110001 = !A, !M
# 001111 = -D
# 110011 = -A, -M
# 011111 = D+1
# 110111 = A+1, M+1
# 001110 = D-1
# 110010 = A-1, M-1
# 000010 = D+A, D+M
# 010011 = D-A, D-M
# 000111 = A-D, M-D
# 000000 = D&A, D&M
# 010101 = D|A, D|M

# D1-D3
# 000 = None
# 001 = M
# 010 = D
# 011 = MD
# 100 = A
# 101 = AM
# 110 = AD
# 111 = AMD

# J1-J3
# 000 = None
# 001 = JGT - >
# 010 = JEQ - =
# 011 = JGE - >=
# 100 = JLT - <
# 101 = JNE - !=
# 110 = JLE - <=
# 111 = JMP - 1
