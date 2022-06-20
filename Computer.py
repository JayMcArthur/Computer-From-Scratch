from Gates import And, Or, Not, DMux4Way, Mux8Way, Mux16
from Memory import RAM32k, PC, Register
from Chips import ALU
import itertools


class CPU:
    def __init__(self):
        self.pc = PC()
        self.regA = Register()
        self.regD = Register()

    def clock(self, instruct, data, reset):
        output = []
        # Get A Reg input for ALU
        wrA = Mux16(self.regA.clock([0] * 16, 0), data, instruct[3])
        # Calculate ALU
        wrB = ALU(self.regD.clock([0] * 16, 0), wrA, *instruct[4:10])
        # Output Data
        output.append(wrB[0])

        # Output write
        output.append(And(instruct[0], instruct[12]))
        # Save to D Reg
        self.regD.clock(wrB[0], And(instruct[0], instruct[11]))

        # IF an Instruction let it in
        wrC = Mux16(instruct, wrB[0], instruct[0])
        # Save to A Reg
        self.regA.clock(wrC, Or(And(instruct[0], instruct[10]), Not(instruct[0])))

        # Address Out
        wrD = self.regA.clock([0] * 16, 0)
        output.append(wrD)

        # Jump Logic
        wrE = DMux4Way(1, wrB[1:])  # LE, LT, EQ, GT
        wrF = Mux8Way(
            0,  # 000 = None
            wrE[3],  # 001 = JGT
            wrE[2],  # 010 = JEQ
            Or(wrE[0], wrE[1]),  # 011 = JGE
            wrE[1],  # 100 = JLT
            Or(wrE[0], wrE[2]),  # 101 = JNE
            wrE[0],  # 110 = JLE
            1,  # 111 = JMP
            instruct[13:]
        )
        wrF = And(wrF, instruct[0])

        # PC Out
        output.append(self.pc.clock(wrD, 1, wrF, reset))

        return output


class Computer:
    def __init__(self, prog):
        self.cpu = CPU()
        # input("CPU Made")
        self.data = RAM32k()
        # input("RAM Made")
        self.program = prog
        self.out = self.cpu.clock([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0] * 16, 1)
        self.outM = self.out[0]
        self.outW = self.out[1]
        self.outA = self.out[2]
        self.run = self.out[3]
        # input("Clock Successful")

    def print_top(self, num):
        inputs = ["".join(seq) for seq in itertools.product("01", repeat=4)]
        print("Register A : " + str(self.cpu.regA.clock([0] * 16, 0)))
        print("Register D : " + str(self.cpu.regD.clock([0] * 16, 0)))
        print("Register PC : " + str(self.cpu.pc.reg.clock([0] * 16, 0)))
        for i in inputs:
            if num:
                print(str("% 2s" % int(i, 2)) + ": " + str(int(''.join(
                    map(str, self.data.clock([0] * 16, [0] * 12 + [int(i[0]), int(i[1]), int(i[2]), int(i[3])], 0))),
                                                               2)))
            else:
                print(str("% 2s" % int(i, 2)) + ": " + str(
                    self.data.clock([0] * 16, [0] * 12 + [int(i[0]), int(i[1]), int(i[2]), int(i[3])], 0)))

    def clock(self):
        self.run = int(''.join(map(str, self.run)), 2)
        self.out = self.cpu.clock(self.program[self.run], self.data.clock([0] * 16, self.outA, 0), 0)
        self.outM = self.out[0]  # ?
        self.outW = self.out[1]  # ?
        self.outA = self.out[2]  # Data to Write
        self.data.clock(self.outM, self.outA, self.outW)
        # printTop()
        self.run = self.out[3]  # Instruction to Goto


program = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],  # REG A = 21
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # A, SAV D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # REG A = 9
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # A+D, SAV M[A], NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # REG A = 4
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1]  # JMP RUN[A] aka infinite loop exit
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
    [1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],  # 11 - D-M, D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],  # 12 - A = 22     >> STOP location
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],  # 13 - D, NONE, JGT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 14 - A = 1
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 15 - M, D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 16 - A = 2
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # 17 - D+M, M, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 18 - A = 1
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0],  # 19 - M+1, M, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # 20 - A = 8       >> LOOP Location
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1],  # 21 - 0, NONE, JMP
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 22 - A = 2       >> STOP
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 23 - M, D, NONE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 24 - A = 1
    [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],  # 25 - D, M, NONE

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],  # 26 - A = 26  >> END Location
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1]  # 27 - 0, NONE, JMP
]

computer = Computer(program)  # Setup computer
print("")
for l in range(50):
    for i in range(2):
        computer.clock()  # Run 2 instructions
    computer.print_top(0)  # print changes
    input()

# If a == 0 then X = D, Y = A
# If a == 1 then X = D, Y = M

# ALU Logic (C1-C6)
# Zx Nx Zy Ny F No = F(x,y)
# 101010 = 0
# 111111 = 1
# 111010 = -1
# 001100 = x
# 110000 = y
# 001101 = !x
# 110001 = !y
# 001111 = -x
# 110011 = -y
# 011111 = x+1
# 110111 = y+1
# 001110 = x-1
# 110010 = y-1
# 000010 = x+y
# 010011 = x-y
# 000111 = y-x
# 000000 = x&y
# 010101 = x|y

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
