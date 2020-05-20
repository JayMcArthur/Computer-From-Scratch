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
    output = []
    temp = HalfAdder(inA16[15], inB16[15])
    output.append(temp.pop())
    for i in range(14, -1, -1):
        temp = (FullAdder(inA16[i], inB16[i], temp.pop()))
        output.append(temp.pop())
    return output[::-1]

def Inc16(input):
    # name = "16-bit Incrementer"
    # IN.16-1 > OUT.16-1
    # value = 140
    one = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,1]
    return Add16(input, one)

def Xor16(inA16, inB16):
    # extra for ease
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
    output.append(Not(Or16Way(output[0]))) # Is Zero
    output.append(output[0][0])            # Is Negative
    return output

