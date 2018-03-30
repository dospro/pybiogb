"""Module that emulates gb-z80 cpu"""
from functools import partial

from pybiogb.cpu.registers import Registers
from pybiogb.cpu.memory.memory import Memory


class Cpu:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.opcodes = {
            # LD nn, n
            0x06: self.ld_n('b_register'),
            0x0E: self.ld_n('c_register'),
            0x16: self.ld_n('d_register'),
            0x1E: self.ld_n('e_register'),
            0x26: self.ld_n('h_register'),
            0x2E: self.ld_n('l_register'),

            # LD r1, r2
            0x7F: self.ld('a_register', 'a_register'),
            0x78: self.ld('a_register', 'b_register'),
            0x79: self.ld('a_register', 'c_register'),
            0x7A: self.ld('a_register', 'd_register'),
            0x7B: self.ld('a_register', 'e_register'),
            0x7C: self.ld('a_register', 'h_register'),
            0x7D: self.ld('a_register', 'l_register'),
            0x7E: self.ld_r_hl('a_register'),

            0x40: self.ld('b_register', 'b_register'),
            0x41: self.ld('b_register', 'c_register'),
            0x42: self.ld('b_register', 'd_register'),
            0x43: self.ld('b_register', 'e_register'),
            0x44: self.ld('b_register', 'h_register'),
            0x45: self.ld('b_register', 'l_register'),
            0x46: self.ld_r_hl('b_register'),

            0x48: self.ld('c_register', 'b_register'),
            0x49: self.ld('c_register', 'c_register'),
            0x4A: self.ld('c_register', 'd_register'),
            0x4B: self.ld('c_register', 'e_register'),
            0x4C: self.ld('c_register', 'h_register'),
            0x4D: self.ld('c_register', 'l_register'),
            0x4E: self.ld_r_hl('c_register'),

            0x50: self.ld('d_register', 'b_register'),
            0x51: self.ld('d_register', 'c_register'),
            0x52: self.ld('d_register', 'd_register'),
            0x53: self.ld('d_register', 'e_register'),
            0x54: self.ld('d_register', 'h_register'),
            0x55: self.ld('d_register', 'l_register'),
            0x56: self.ld_r_hl('d_register'),

            0x58: self.ld('e_register', 'b_register'),
            0x59: self.ld('e_register', 'c_register'),
            0x5A: self.ld('e_register', 'd_register'),
            0x5B: self.ld('e_register', 'e_register'),
            0x5C: self.ld('e_register', 'h_register'),
            0x5D: self.ld('e_register', 'l_register'),
            0x5E: self.ld_r_hl('e_register'),

            0x60: self.ld('h_register', 'b_register'),
            0x61: self.ld('h_register', 'c_register'),
            0x62: self.ld('h_register', 'd_register'),
            0x63: self.ld('h_register', 'e_register'),
            0x64: self.ld('h_register', 'h_register'),
            0x65: self.ld('h_register', 'l_register'),
            0x66: self.ld_r_hl('h_register'),

            0x68: self.ld('l_register', 'b_register'),
            0x69: self.ld('l_register', 'c_register'),
            0x6A: self.ld('l_register', 'd_register'),
            0x6B: self.ld('l_register', 'e_register'),
            0x6C: self.ld('l_register', 'h_register'),
            0x6D: self.ld('l_register', 'l_register'),
            0x6E: self.ld_r_hl('l_register'),

            0x70: self.ld_hl_r('b_register'),
            0x71: self.ld_hl_r('c_register'),
            0x72: self.ld_hl_r('d_register'),
            0x73: self.ld_hl_r('e_register'),
            0x74: self.ld_hl_r('h_register'),
            0x75: self.ld_hl_r('l_register'),
            0x36: self.ld_hl_n,

            0x0A: self.ld_a_rr('bc_register'),
            0x1A: self.ld_a_rr('de_register'),
            0xFA: self.ld_a_nn,
            0x3E: self.ld_n('a_register'),

            0x47: self.ld('register_b', 'register_b'),
            0x4F: self.ld('register_c', 'register_b'),
            0x57: self.ld('register_d', 'register_b'),
            0x5F: self.ld('register_e', 'register_b'),
            0x67: self.ld('register_h', 'register_b'),
            0x6F: self.ld('register_l', 'register_b'),

            0x02: self.ld_rr_a('register_bc'),
            0x12: self.ld_rr_a('register_de'),
            0x77: self.ld_rr_a('register_hl'),
            0xEA: self.ld_nn_a,

            0xF2: self.ld_a_ff00_plus_c,
            0xE2: self.ld_ff00_plus_c_a,

            0x3A: self.ld_a_hl_dec,
            0x32: self.ld_hl_a_dec,
            0x2A: self.ld_a_hl_inc,
            0x22: self.ld_hl_a_inc,

            0x87: partial(self.add, self.registers.a_register),
            0x80: partial(self.add, self.registers.b_register),
            0x81: partial(self.add, self.registers.c_register),
            0x82: partial(self.add, self.registers.d_register),
            0x83: partial(self.add, self.registers.e_register),
            0x84: partial(self.add, self.registers.a_register),
            0x85: partial(self.add, self.registers.l_register),
            0x86: partial(self.add, self.memory.read_byte(self.registers.hl_register)),
            0xC6: partial(self.add, self.read_next_byte()),

            0x8F: partial(self.adc, self.registers.a_register),
            0x88: partial(self.adc, self.registers.b_register),
            0x89: partial(self.adc, self.registers.c_register),
            0x8A: partial(self.adc, self.registers.d_register),
            0x8B: partial(self.adc, self.registers.e_register),
            0x8C: partial(self.adc, self.registers.a_register),
            0x8D: partial(self.adc, self.registers.l_register),
            0x8E: partial(self.adc, self.memory.read_byte(self.registers.hl_register)),
            0xCE: partial(self.adc, self.read_next_byte()),

            0x97: partial(self.sub, self.registers.a_register),

            0x3D: partial(self.dec, 'a_register')
        }

    def execute_opcode(self):
        opcode = self.read_next_byte()
        self.opcodes[opcode]()

    def read_next_byte(self):
        result = self.memory.read_byte(self.registers.pc_register)
        self.registers.pc_register += 1
        return result

    def adc(self, value):
        new_value = self.registers.a_register + value + self.registers.c_flag
        self.registers.z_flag = (new_value & 0xFF) == 0
        self.registers.n_flag = 0
        half_value = (self.registers.a_register & 0xF) + (value & 0xF) + self.registers.c_flag
        self.registers.h_flag = half_value > 0xF
        self.registers.c_flag = new_value > 0xFF
        self.registers.a_register = new_value & 0xFF

    def add(self, value):
        new_value = self.registers.a_register + value
        half_value = (self.registers.a_register & 0xF) + (value & 0xF)

        self.registers.z_flag = (new_value & 0xFF) == 0
        self.registers.n_flag = False
        self.registers.h_flag = half_value > 0xF
        self.registers.c_flag = new_value > 0xFF

        self.registers.a_register = (new_value & 0xFF)

    def add_hl(self, value):
        self.registers.n_flag = False
        self.registers.h_flag = ((self.registers.hl_register & 0xFFF) + (value & 0xFFF)) > 0xFFF
        self.registers.c_flag = (self.registers.hl_register + value) > 0xFFFF
        self.registers.hl_register += value

    def add_sp(self, signed_value):  # Signed value
        unsigned_value = signed_value
        if signed_value < 0:
            unsigned_value += 256
        self.registers.c_flag = (self.registers.sp_register & 0xFF) + unsigned_value > 0xFF
        self.registers.h_flag = ((self.registers.sp_register & 0xF) + (unsigned_value & 0xF)) > 0xF
        self.registers.sp_register += signed_value
        self.registers.z_flag = False
        self.registers.n_flag = False

    def z80_and(self, value):
        self.registers.a_register &= value
        self.registers.z_flag = self.registers.a_register == 0
        self.registers.n_flag = False
        self.registers.h_flag = True
        self.registers.c_flag = False

    def bit(self, bit_position, register_value):
        bit_position >>= 3
        self.registers.z_flag = (register_value & (1 << bit_position)) == 0
        self.registers.n_flag = False
        self.registers.h_flag = True

    def call(self, condition, address):
        if condition:
            self.z80_push(self.registers.pc_register)
            self.registers.pc_register = address

    def cp(self, value):
        self.registers.z_flag = self.registers.a_register == value
        self.registers.n_flag = True
        self.registers.h_flag = (self.registers.a_register & 0xF) < (value & 0xF)
        self.registers.c_flag = self.registers.a_register < value

    def daa(self):
        new_value = self.registers.a_register
        if self.registers.n_flag:
            if self.registers.h_flag:
                new_value = (new_value - 6) & 0xFF
            if self.registers.c_flag:
                new_value -= 0x60
        else:
            if self.registers.h_flag or (new_value & 0xF) > 9:
                new_value += 6
            if self.registers.c_flag or (new_value > 0x9F):
                new_value += 0x60

        if new_value & 0x100 == 0x100:
            self.registers.c_flag = True

        self.registers.a_register = new_value & 0xFF
        self.registers.z_flag = self.registers.a_register == 0
        self.registers.h_flag = False

    def dec(self, register_name):
        register = getattr(self.registers, register_name)
        self.registers.z_flag = register == 1
        self.registers.n_flag = True
        self.registers.h_flag = (register & 0xF) == 0
        setattr(self.registers, register_name, register - 1)

    def dec_16(self, register_name):
        register = getattr(self.registers, register_name)
        setattr(self.registers, register_name, register - 1)

    def inc(self, register_name):
        register = getattr(self.registers, register_name)
        self.registers.z_flag = register == 0xFF
        self.registers.n_flag = False
        self.registers.h_flag = (register & 0xF) == 0xF
        setattr(self.registers, register_name, register + 1)

    def inc_16(self, register_name):
        register = getattr(self.registers, register_name)
        setattr(self.registers, register_name, register + 1)

    def jp(self, condition, address):
        if condition:
            self.registers.pc_register = address

    def jr(self, condition, value):
        signed_value = value
        if value > 127:
            signed_value = value - 256
        if condition:
            self.registers.pc_register += signed_value

    def ld_hl(self, signed_value):
        unsigned_value = signed_value
        if signed_value < 0:
            unsigned_value += 256
        self.registers.c_flag = ((self.registers.sp_register & 0xFF) + unsigned_value) > 0xFF
        self.registers.h_flag = ((self.registers.sp_register & 0xF) + (unsigned_value & 0xF) > 0xF)
        self.registers.z_flag = False
        self.registers.n_flag = False
        self.registers.hl_register = self.registers.sp_register + signed_value

    def ld_nn_sp(self, value):
        self.memory.write_byte(value, self.registers.sp_register & 0xFF)
        self.memory.write_byte(value + 1, self.registers.sp_register >> 8)

    def z80_or(self, value):
        self.registers.a_register |= value
        self.registers.z_flag = self.registers.a_register == 0
        self.registers.n_flag = False
        self.registers.h_flag = False
        self.registers.c_flag = False

    def z80_pop(self, register_name):
        high_byte = self.memory.read_byte(self.registers.sp_register)
        self.registers.sp_register += 1
        low_byte = self.memory.read_byte(self.registers.sp_register)
        self.registers.sp_register += 1
        result = (high_byte << 8) | low_byte
        setattr(self.registers, register_name, result)

    def z80_push(self, register_name):
        register_value = getattr(self.registers, register_name)
        self.registers.sp_register -= 1
        self.memory.write_byte(self.registers.sp_register, register_value >> 8)
        self.registers.sp_register -= 1
        self.memory.write_byte(self.registers.sp_register, register_value & 0xFF)

    def ld(self, dst_register, src_register):
        registers = vars(self.registers)

        def real_ld():
            registers[dst_register] = registers[src_register]

        return real_ld

    def ld_n(self, dst_register):
        registers = vars(self.registers)

        def real_ld_n():
            registers[dst_register] = self.read_next_byte()

        return real_ld_n

    def ld_r_hl(self, dst_register):
        registers = vars(self.registers)

        def real_r_ld():
            registers[dst_register] = self.memory.read_byte(self.registers.hl_register)

        return real_r_ld

    def ld_hl_r(self, src_register):
        registers = vars(self.registers)

        def real_ld_hl_r():
            self.memory.write_byte(self.registers.hl_register, registers[src_register])

        return real_ld_hl_r

    def ld_hl_n(self):
        self.memory.write_byte(self.registers.hl_register, self.read_next_byte())

    def ld_a_rr(self, src_register):
        registers = vars(self.registers)

        def real_a_rr():
            self.registers.a_register = self.memory.read_byte(registers[src_register])

        return real_a_rr

    def ld_a_nn(self):
        low_byte = self.read_next_byte()
        high_byte = self.read_next_byte()
        address = ((high_byte << 8) | low_byte) & 0xFFFF
        self.registers.a_register = self.memory.read_byte(address)

    def ld_rr_a(self, dst_register):
        registers = vars(self.registers)

        def real_ld_rr_a():
            self.memory.write_byte(registers[dst_register], self.registers.a_register)

        return real_ld_rr_a

    def ld_nn_a(self):
        low_byte = self.read_next_byte()
        high_byte = self.read_next_byte()
        address = ((high_byte << 8) | low_byte) & 0xFFFF
        self.memory.write_byte(address, self.registers.a_register)

    def ld_a_ff00_plus_c(self):
        self.registers.a_register = self.memory.read_byte(0xFF00 + self.registers.c_register)

    def ld_ff00_plus_c_a(self):
        self.memory.write_byte(0xFF00 + self.registers.c_register, self.registers.a_register)

    def ld_a_hl_dec(self):
        self.registers.a_register = self.memory.read_byte(self.registers.hl_register)
        self.registers.a_register -= 1

    def ld_hl_a_dec(self):
        self.memory.write_byte(self.registers.hl_register, self.registers.a_register)
        self.registers.hl_register -= 1

    def ld_a_hl_inc(self):
        self.registers.a_register = self.memory.read_byte(self.registers.hl_register)
        self.registers.a_register -= 1

    def ld_hl_a_inc(self):
        self.memory.write_byte(self.registers.hl_register, self.registers.a_register)
        self.registers.hl_register -= 1

    def sub(self, value):
        self.registers.z_flag = self.registers.a_register == value
        self.registers.n_flag = True
        self.registers.h_flag = (value & 0xF) > (self.registers.a_register & 0xF)
        self.registers.c_flag = value > self.registers.a_register
        self.registers.a_register = (self.registers.a_register - value) & 0xFF
