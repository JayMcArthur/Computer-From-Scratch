from itertools import product
import os

from Chips import ALU
from Gates import Nor, And, Or, Not, Mux16
from Memory import RAM32k, PC, Register


class CPU:
    # name = CPU
    # value = 1452
    def __init__(self):
        self.pc = PC()
        self.regA = Register()
        self.regD = Register()

    def clock(self, instruct, memory, reset):
        # Label instruction and determine type
        [TYPE, NA1, NA2, AOrM, Zx, Nx, Zy, Ny, F, No, SaveA, SaveD, SaveM, JLT, JEQ, JGT] = Mux16([0] * 16, instruct,
                                                                                                  instruct[0]) # Excluding this from value as its just for naming purposes
        # Get Reg D
        xIn = self.regD.clock([0] * 16, 0)
        # Get Reg A or M
        yIn = Mux16(self.regA.clock([0] * 16, 0), memory, AOrM)

        # Calculate ALU
        [aluOut, isZero, isNeg] = ALU(xIn, yIn, Zx, Nx, Zy, Ny, F, No)

        # Save Reg D
        regDOut = self.regD.clock(aluOut, SaveD)
        # Save Reg A
        regAOut = self.regA.clock(Mux16(instruct, aluOut, TYPE), Or(Not(TYPE), SaveA))

        # Jump Logic
        Jump = Or(Or(And(isNeg, JLT), And(isZero, JEQ)), And(Nor(isZero, isNeg), JGT))

        # PC update
        PCOut = self.pc.clock(regAOut, 1, Jump, reset)

        return [aluOut, SaveM, regAOut[1:], PCOut]


class Computer:
    # name = Computer
    # value = 1452 + 4718592
    def __init__(self, prog):
        self.cpu = CPU()
        # input("CPU Made")
        self.data = RAM32k()
        # input("RAM Made")
        self.program = prog
        self.out = self.cpu.clock([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0] * 16, 1)
        self.run = self.out[3]
        # input("Clock Successful")

    def print_top(self, decimal, amount):
        os.system('cls' if os.name == 'nt' else 'clear')
        inputs = ["".join(seq) for seq in product("01", repeat=amount)]
        print("Register A : " + str(self.cpu.regA.clock([0] * 16, 0)))
        print("Register D : " + str(self.cpu.regD.clock([0] * 16, 0)))
        print("Register PC : " + str(self.cpu.pc.reg.clock([0] * 16, 0)))
        for i in inputs:
            if decimal:
                print(str("% 2s" % int(i, 2)) + ": " + str(int(''.join(
                    map(str, self.data.clock([0] * 16, [0] * (15 - amount) + [*map(int, list(i))], 0))), 2)))
            else:
                print(str("% 2s" % int(i, 2)) + ": " + str(
                    self.data.clock([0] * 16, [0] * (15 - amount) + [*map(int, list(i))], 0)))
        input()

    def clock(self):
        self.run = int(''.join(map(str, self.run)), 2)
        if self.run > len(self.program) - 1: exit(0)
        self.out = self.cpu.clock(self.program[self.run], self.data.clock([0] * 16, self.out[2], 0), 0)
        self.data.clock(self.out[0], self.out[2], self.out[1])
        self.run = self.out[3]  # Instruction to Goto


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
