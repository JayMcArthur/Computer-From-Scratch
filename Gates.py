#
# PREMADE GATES
#

def Nand(inA, inB):
    # name = 'Nand Gate'
    # IN, IN > OUT
    # value = 1
    return int(not (inA and inB))


#
# Elementary Logic
#

def Not(input):
    # name = "Not Gate"
    # IN > OUT
    # value = 1
    return Nand(input, input)


def And(inA, inB):
    # name = "And Gate"
    # IN, IN > OUT
    # value = 2
    return Not(Nand(inA, inB))


def Or(inA, inB):
    # name = "Or Gate"
    # IN, IN > OUT
    # value = 3
    return Nand(Not(inA), Not(inB))


def Nor(inA, inB):
    # name = "Nor Gate"
    # IN, IN > OUT
    # value = 4
    return Not(Or(inA, inB))


def Xor(inA, inB):
    # name = "Xor Gate"
    # IN, IN > OUT
    # value = 4
    wire = Nand(inA, inB)
    return Nand(Nand(inA, wire), Nand(inB, wire))


def Mux(inA, inB, sel):
    # name = "Multiplexor"
    # IN, IN, SEL > OUT
    # value = 4
    return Nand(Nand(inA, Not(sel)), Nand(inB, sel))


def DMux(input, sel):
    # name = "Demultiplexor"
    # IN, SEL > OUT, OUT
    # value = 5
    return [And(input, Not(sel)), And(input, sel)]


#
# 16-bit Logic
#

def Not16(in16):
    # name = "16-bit Not"
    # 16xIN > 16xOUT
    # value = 16
    output = []
    for i in range(16):
        output.append(Not(in16[i]))
    return output


def And16(inA16, inB16):
    # name = "16-bit And"
    # 16xIN, 16xIN > 16xOUT
    # value = 32
    output = []
    for i in range(16):
        output.append(And(inA16[i], inB16[i]))
    return output


def Or16(inA16, inB16):
    # name = "16-bit And"
    # 16xIN, 16xIN > 16xOUT
    # value = 48
    output = []
    for i in range(16):
        output.append(Or(inA16[i], inB16[i]))
    return output


def Mux16(inA16, inB16, sel):
    # name = "16-bit Multiplexor"
    # 16xIN, 16xIN, SEL > 16xOUT
    # value = 64
    output = []
    for i in range(16):
        output.append(Mux(inA16[i], inB16[i], sel))
    return output


#
# Multi-way Logic
#

def Or8Way(in8):
    # Extra for ease
    return Or(Or(Or(in8[0], in8[1]), Or(in8[2], in8[3])), Or(Or(in8[4], in8[5]), Or(in8[6], in8[7])))


def Or16Way(in16):
    # name = "16 Way Or"
    # 16xIN > OUT
    # value = 45
    return Or(Or8Way(in16[:8]), Or8Way(in16[8:]))


def Mux4Way(inA, inB, inC, inD, sel):
    # name = "4 Way Mux"
    # IN, IN, IN, IN, SEL.2, SEL.1 > OUT
    # value = 12
    return Mux(Mux(inA, inB, sel[1]), Mux(inC, inD, sel[1]), sel[0])


def Mux4Way16(inA16, inB16, inC16, inD16, sel):
    # name = "4 Way 16-bit Mux"
    # 16xIN, 16xIN, 16xIN, 16xIN, SEL.2, SEL.1 > 16xOUT
    # value = 192
    return Mux16(Mux16(inA16, inB16, sel[1]), Mux16(inC16, inD16, sel[1]), sel[0])


def Mux8Way(inA, inB, inC, inD, inE, inF, inG, inH, sel):
    # name = "8 Way Mux"
    # 8xIN, SEL.3, SEL.2, SEL.1 > OUT
    # value = 28
    return Mux(Mux4Way(inA, inB, inC, inD, sel[1:]), Mux4Way(inE, inF, inG, inH, sel[1:]), sel[0])


def Mux8Way16(inA16, inB16, inC16, inD16, inE16, inF16, inG16, inH16, sel):
    # name = "8 Way 16-bit Mux"
    # 8x [16xIN], SEL.3, SEL.2, SEL.1 > 16xOUT
    # value = 448
    return Mux16(Mux4Way16(inA16, inB16, inC16, inD16, sel[1:]), Mux4Way16(inE16, inF16, inG16, inH16, sel[1:]), sel[0])


def DMux4Way(input, sel):
    # name = "4 Way Demux"
    # IN, SEL.2, SEL.1 > 4xOUT
    # value = 15
    wireA = DMux(input, sel[0])
    return DMux(wireA[0], sel[1]) + DMux(wireA[1], sel[1])


def DMux8Way(input, sel):
    # name = "8 Way Demux"
    # 16xIN, SEL.3, SEL.2, SEL.1 > 8xOUT
    # value = 35
    wireA = DMux(input, sel[0])
    return DMux4Way(wireA[0], sel[1:]) + DMux4Way(wireA[1], sel[1:])
