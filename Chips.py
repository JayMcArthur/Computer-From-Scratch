from Gates import Nand, Not, Xor, And16, Mux16, Or16Way


def HalfAdder(inA, inB):
    # name = "Half Adder"
    # IN, IN > OUT.2, OUT.1
    # value = 5
    output = []
    inC = Nand(inA, inB)
    output.append(Not(inC))
    output.append(Nand(Nand(inA, inC), Nand(inB, inC)))
    return output


def FullAdder(inA, inB, carry):
    # name = "Full Adder"
    # IN, IN, CARRY > OUT.2, OUT.1
    # value = 9
    output = []
    wrA = Nand(inA, inB)
    wrB = Nand(Nand(inA, wrA), Nand(inB, wrA))
    wrC = Nand(carry, wrB)
    output.append(Nand(wrA, wrC))
    output.append(Nand(Nand(wrB, wrC), Nand(carry, wrC)))
    return output


def Add16(inA16, inB16):
    # name = "16-bit Adder"
    # IN.16-1, IN.16-1 > OUT.16-1
    # value = 140
    output = [0] * 16
    output = output[0:14] + HalfAdder(inA16[15], inB16[15])
    output = output[0:13] + FullAdder(inA16[14], inB16[14], output[14]) + output[15:]
    output = output[0:12] + FullAdder(inA16[13], inB16[13], output[13]) + output[14:]
    output = output[0:11] + FullAdder(inA16[12], inB16[12], output[12]) + output[13:]
    output = output[0:10] + FullAdder(inA16[11], inB16[11], output[11]) + output[12:]
    output = output[0:9] + FullAdder(inA16[10], inB16[10], output[10]) + output[11:]
    output = output[0:8] + FullAdder(inA16[9], inB16[9], output[9]) + output[10:]
    output = output[0:7] + FullAdder(inA16[8], inB16[8], output[8]) + output[9:]
    output = output[0:6] + FullAdder(inA16[7], inB16[7], output[7]) + output[8:]
    output = output[0:5] + FullAdder(inA16[6], inB16[6], output[6]) + output[7:]
    output = output[0:4] + FullAdder(inA16[5], inB16[5], output[5]) + output[6:]
    output = output[0:3] + FullAdder(inA16[4], inB16[4], output[4]) + output[5:]
    output = output[0:2] + FullAdder(inA16[3], inB16[3], output[3]) + output[4:]
    output = output[0:1] + FullAdder(inA16[2], inB16[2], output[2]) + output[3:]
    output = FullAdder(inA16[1], inB16[1], output[1]) + output[2:]
    output = FullAdder(inA16[0], inB16[0], output[0])[1:] + output[1:]
    return output


def Inc16(input):
    # name = "16-bit Incrementer"
    # IN.16-1 > OUT.16-1
    # value = 140
    one = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    return Add16(input, one)


def Xor16(inA16, inB16):
    # extra for ease
    # value = 64
    output = []
    for i in range(16):
        output.append(Xor(inA16[i], inB16[i]))
    return output


def ALU(inA16, inB16, ZX, NX, ZY, NY, F, NO):
    # name = "ALU"
    # IN.16-1, IN.16-1, ZX, NX, ZY, NY, F, NO > OUT.16-1, ZR, NG
    # value = 540
    output = []
    inA16 = And16(inA16, [Not(ZX)] * 16)
    inA16 = Xor16(inA16, [NX] * 16)
    inB16 = And16(inB16, [Not(ZY)] * 16)
    inB16 = Xor16(inB16, [NY] * 16)

    out = Mux16(And16(inA16, inB16), Add16(inA16, inB16), F)
    output.append(Xor16(out, [NO] * 16))
    output.append(Not(Or16Way(output[0])))  # Is Zero
    output.append(output[0][0])  # Is Negative
    return output
