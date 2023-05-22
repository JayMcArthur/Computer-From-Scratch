#
# PREMADE GATES
#

def Nand(a, b):
    # name = 'Nand Gate'
    # IN, IN > OUT
    # value = 1
    return int(not (a and b))


#
# Elementary Logic
#

def Not(a):
    # name = "Not Gate"
    # IN > OUT
    # value = 1
    return Nand(a, a)


def And(a, b):
    # name = "And Gate"
    # IN, IN > OUT
    # value = 2
    return Not(Nand(a, b))


def Or(a, b):
    # name = "Or Gate"
    # IN, IN > OUT
    # value = 3
    return Nand(Not(a), Not(b))


def Nor(a, b):
    # name = "Nor Gate"
    # IN, IN > OUT
    # value = 4
    return Not(Or(a, b))


def Xor(a, b):
    # name = "Xor Gate"
    # IN, IN > OUT
    # value = 4
    n1 = Nand(a, b)
    return Nand(Nand(a, n1), Nand(b, n1))


def Selector(a, b, sel, selI):
    # name = "Selector"
    # IN, IN, SEL > OUT
    # value = 3
    return Nand(Nand(a, selI), Nand(b, sel))


def Mux(a, b, sel):
    # name = "Multiplexor"
    # IN, IN, SEL > OUT
    # value = 4
    return Nand(Nand(a, Not(sel)), Nand(b, sel))


#
# 16-bit Logic
#

def Nand16(a16, b16):
    # name = "16-bit Nand"
    # 16xIN, 16xIN > 16xOUT
    # value = 16
    output = []
    for i in range(16):
        output.append(Nand(a16[i], b16[i]))
    return output


def Not16(a16):
    # name = "16-bit Not"
    # 16xIN > 16xOUT
    # value = 16
    output = []
    for i in range(16):
        output.append(Not(a16[i]))
    return output


def And16(a16, b16):
    # name = "16-bit And"
    # 16xIN, 16xIN > 16xOUT
    # value = 32
    output = []
    for i in range(16):
        output.append(And(a16[i], b16[i]))
    return output


def Or16(a16, b16):
    # name = "16-bit Or"
    # 16xIN, 16xIN > 16xOUT
    # value = 48
    output = []
    for i in range(16):
        output.append(Or(a16[i], b16[i]))
    return output


def Xor16(a16, b16):
    # name = "16-bit Xor"
    # 16xIN, 16xIN > 16xOUT
    # value = 64
    output = []
    for i in range(16):
        output.append(Xor(a16[i], b16[i]))
    return output


def Selector16(a16, b16, sel, selI):
    # name = "16-bit Multiplexor"
    # 16xIN, 16xIN, SEL > 16xOUT
    # value = 48
    output = []
    for i in range(16):
        output.append(Selector(a16[i], b16[i], sel, selI))
    return output


def Mux16(a16, b16, sel):
    # name = "16-bit Multiplexor"
    # 16xIN, 16xIN, SEL > 16xOUT
    # value = 49
    selI = Not(sel)
    return Selector16(a16, b16, sel, selI)


#
# Multi-way Logic
#

def Or8Way(a8):
    # name = '8 way Or"
    # value = 21
    return Or(Or(Or(a8[0], a8[1]), Or(a8[2], a8[3])), Or(Or(a8[4], a8[5]), Or(a8[6], a8[7])))

