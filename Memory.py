from Gates import Mux, Mux16
from Chips import Inc16
import itertools

#
# PREMADE CHIPS
#

class DFF:
    def __init__(self):
        self.mem = 0
    def set(self, input):
        self.mem = input
    def pull(self):
        return self.mem

def layer(func, size):
    if size > 1:
        out = [layer(func, size-1), layer(func, size-1)]
    else:
        out = [func(), func()]
    return out

def ToIndex(i):
    return [[[[i[15],i[14]],[i[13],i[12]]],[[i[11],i[10]],[i[9],i[8]]]],[[[i[7],i[6]],[i[5],i[4]]],[[i[3],i[2]],[i[1],i[0]]]]]
 

#
# MEMORY CHIPS
#

class Bit:
    # name = "1-bit Register"
    def __init__(self):
        self.DFF_Chip = DFF()
    def clock(self, input, load):
        self.DFF_Chip.set(int(Mux(self.DFF_Chip.pull(), input, load)))
    def pull(self):
        return self.DFF_Chip.pull()

class Register:
    # name = "16-bit Register"
    inputs = ["".join(seq) for seq in itertools.product("01", repeat=4)]
    def __init__(self):
        self.Bits = layer(Bit, 4) 
    def clock(self, in16, load, pull):
        in16 = ToIndex(in16)
        output = []
        for i in self.inputs:
            self.Bits[int(i[0])][int(i[1])][int(i[2])][int(i[3])].clock(in16[int(i[0])][int(i[1])][int(i[2])][int(i[3])], load)
            output.append(self.Bits[int(i[0])][int(i[1])][int(i[2])][int(i[3])].pull())
        if pull:
            return output[::-1]
        else:
            return None

class RAM8:
    # name = "16-bit 8 Register Memory"
    def __init__(self):
        self.reg = layer(Register, 3)
    def clock(self, in16, k, load, pull):
        return self.reg[k[0]][k[1]][k[2]].clock(in16, load, pull)
        
class RAM64:
    #name = "16-bit 64 Register Memory"
    def __init__(self):
        self.reg = layer(RAM8, 3)
    def clock(self, in16, k, load, pull):
        return self.reg[k[0]][k[1]][k[2]].clock(in16, k[3:], load, pull)

class RAM512:
    #name = "16-bit 512 Register Memory"
    def __init__(self):
        self.reg = layer(RAM64, 3)
    def clock(self, in16, k, load, pull):
        return self.reg[k[0]][k[1]][k[2]].clock(in16, k[3:], load, pull)

class RAM4k:
    #name = "16-bit 4096 Register Memory"
    def __init__(self):
        self.reg = layer(RAM512, 3)
    def clock(self, in16, k, load, pull):
        return self.reg[k[0]][k[1]][k[2]].clock(in16, k[3:], load, pull)

class RAM16k:
    # name = "16-bit 16,384 Register Memory"
    def __init__(self):
        self.reg = layer(RAM4k, 3)
    def clock(self, in16, k, load, pull):
        return self.reg[k[0]][k[1]][k[2]].clock(in16, k[3:], load, pull)

class RAM32k:
    # name = "16-bit 32,768 Register Memory"
    def __init__(self):
        self.reg = layer(RAM16k, 1)
    def clock(self, in16, k, load, pull):
        return self.reg[k[0]].clock(in16, k[1:], load, pull)

class PC:
    # name = "16-bit Program Counter"
    def __init__(self):
        self.reg = Register()
    def clock(self, in16, inc, load, pull, reset):
        output = self.reg.clock([0]*16, 0, 1)
        output = Mux16(output, Inc16(output), inc)
        output = Mux16(output, in16, load)
        output = Mux16(output, [0]*16, reset)
        self.reg.clock(output, 1, 0)
        if pull:
            return output
        else:
            return None