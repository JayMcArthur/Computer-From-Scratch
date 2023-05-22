from Gates import Mux, Mux16
from Chips import Inc16


#
# Helper Functions
#
def layer(func, size):
    if size > 1:
        out = [layer(func, size-1), layer(func, size-1)]
    else:
        out = [func(), func()]
    return out


#
# MEMORY CHIPS
#
class Bit:
    # name = "bit Register"
    # value = 4
    def __init__(self):
        self.DFF = 0

    def clock(self, data, save):
        self.DFF = int(Mux(self.DFF, data, save))
        return self.DFF


class Register:
    # name = "16-bit Register"
    # value = 144
    def __init__(self):
        self.bits = []
        for i in range(16):
            self.bits.append(Bit())

    def clock(self, in16, load):
        output = []
        for index, b in enumerate(self.bits):
            output.append(b.clock(in16[index], load))
        return output


class RAM8:
    # name = "16-bit 8 Register Memory"
    # value = 1152
    def __init__(self):
        self.regs = layer(Register, 3)

    def clock(self, in16, address, load):
        return self.regs[address[0]][address[1]][address[2]].clock(in16, load)


class RAM64:
    # name = "16-bit 64 Register Memory"
    # value = 9216
    def __init__(self):
        self.regs = layer(RAM8, 3)

    def clock(self, in16, address, load):
        return self.regs[address[0]][address[1]][address[2]].clock(in16, address[3:], load)


class RAM512:
    # name = "16-bit 512 Register Memory"
    # value = 73 728
    def __init__(self):
        self.regs = layer(RAM64, 3)

    def clock(self, in16, address, load):
        return self.regs[address[0]][address[1]][address[2]].clock(in16, address[3:], load)


class RAM4k:
    # name = "16-bit 4096 Register Memory"
    # value = 589 824
    def __init__(self):
        self.regs = layer(RAM512, 3)

    def clock(self, in16, address, load):
        return self.regs[address[0]][address[1]][address[2]].clock(in16, address[3:], load)


class RAM32k:
    # name = "16-bit 32,768 Register Memory"
    # value = 4 718 592
    def __init__(self):
        self.regs = layer(RAM4k, 3)

    def clock(self, in16, address, load):
        return self.regs[address[0]][address[1]][address[2]].clock(in16, address[3:], load)


class RAM64k:
    # name = "16-bit 65,536 Register Memory"
    # value = 9 437 184
    def __init__(self):
        self.regs = layer(RAM32k, 1)

    def clock(self, in16, address, load):
        return self.regs[address[0]].clock(in16, address[1:], load)
