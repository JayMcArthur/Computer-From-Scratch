from Gates import Nand, Not, And, Xor, Xor16, Mux16, Selector16, Or8Way


def HalfAdder(a, b):
    # name = "Half Adder"
    # IN, IN > OUT.2, OUT.1
    # value = 5
    output = []
    n1 = Nand(a, b)
    output.append(Not(n1))
    output.append(Nand(Nand(a, n1), Nand(b, n1)))
    return output


def Inc16(a16):
    # name = "16-bit Incrementer"
    # IN.16-1 > OUT.16-1
    # value = 75
    output = [0] * 16
    output[15] = Not(a16[15])
    n1 = a16[15]
    for i in range(14, 0, -1):
        n1, output[i] = HalfAdder(a16[i], n1)
    output[0] = Xor(a16[0], n1)
    return output


def o41UnaryALU1(zIn, n, zI, a):
    # value = 4
    return Nand(Nand(zIn, a), Nand(n, Nand(zI, a)))


def o41UnaryALU16(zIn, n, zI, inA16):
    # value = 64
    output = []
    for i in range(16):
        output.append(o41UnaryALU1(zIn, n, zI, inA16[i]))
    return output


def Unary_ALU(z, n, a16):
    # name = "Unary ALU"
    # IN, IN, INx16 > OUTx16
    # value = 68
    zI = Not(z)
    nI = Not(n)
    return o41UnaryALU16(And(zI, nI), n, zI, a16)


def Nand_and_xor(a, b):
    #
    #
    # value = 4
    nand = Nand(a, b)
    return [nand, Nand(Nand(a, nand), Nand(b, nand))]


def Nand_xor_adder(a, b, c):
    #
    #
    # value = 9
    nand = Nand_and_xor(a, b)
    xor = Nand_and_xor(nand[1], c)
    return [nand[0], Nand(nand[0], xor[0]), xor[1]]


def Nand_16_add_16(a16, b16):
    #
    #
    # value 139
    nand_out = [0] * 16
    add_out = [0] * 16
    temp = Nand_and_xor(a16[15], b16[15])
    add_out[15] = temp[1]
    nand_out[15] = temp[0]
    hold = Not(temp[0])
    for i in range(14, 0, -1):
        temp = Nand_xor_adder(a16[i], b16[i], hold)
        add_out[i] = temp[2]
        hold = temp[1]
        nand_out[i] = temp[0]
    temp = Nand_and_xor(a16[0], b16[0])
    add_out[0] = Xor(temp[1], hold)
    nand_out[0] = temp[0]
    return [nand_out, add_out]


def ALU(a16, b16, ZX, NX, ZY, NY, F, NO):
    # name = "Arithmetic Logic Unit"
    # IN, OPC.1, OPC.0, IN, IN, INx16, INx16 > OUTx16
    # value = 392
    a16 = Unary_ALU(ZX, NX, a16)
    b16 = Unary_ALU(ZY, NY, b16)
    wireA = Nand_16_add_16(a16, b16)
    FI = Not(F)
    NO = [Xor(FI, NO)] * 16
    return Xor16(Selector16(wireA[0], wireA[1], F, FI), NO)


def Condition(lt, eq, gt, a16):
    # name = "Condition Checker"
    # INx16, INx16 > OUT, OUT, OUT
    # value = 50
    ors = Or8Way([Or8Way(a16[1:9])] + a16[9:])
    part = Nand(Nand(eq, Not(ors)), Nand(gt, ors))
    return Nand(Nand(part, Not(a16[0])), Nand(lt, a16[0]))


def ALU_Instruction(Ix16, ax16, dx16, mx16):
    # name
    # value = 491
    c = 0
    output = []
    output.append(ALU(dx16, Mux16(ax16, mx16, Ix16[3]), Ix16[4], Ix16[5], Ix16[6], Ix16[7], Ix16[8], Ix16[9]))
    output.append(Ix16[10:13])
    output.append(Condition(Ix16[13], Ix16[14], Ix16[15], output[0]))
    return output


def CPU(Ix16, Ax16, Dx15, Mx15):
    # Value = 548
    output = []
    alu_r = ALU_Instruction(Ix16, Ax16, Dx15, Mx15)
    I0I = Not(Ix16[0])
    output.append(Selector16(Ix16, alu_r[0], Ix16[0], I0I))
    output.append([Nand(Ix16[0], Not(alu_r[1][0])), And(Ix16[0], alu_r[1][1]), And(Ix16[0], alu_r[1][2])])
    output.append(And(Ix16[0], alu_r[2]))
    return output