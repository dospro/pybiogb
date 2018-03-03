"""Module that emulates gb-z80 cpu"""
from functools import partial

from pybiogb.cpu.registers import Registers
from pybiogb.cpu.memory.memory import Memory


class Cpu:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.opcodes = {
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
        pass

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

    def ld(self, src_name, dst_name):
        setattr(self.registers, dst_name, getattr(self.registers, src_name))

    def sub(self, value):
        self.registers.z_flag = self.registers.a_register == value
        self.registers.n_flag = True
        self.registers.h_flag = (value & 0xF) > (self.registers.a_register & 0xF)
        self.registers.c_flag = value > self.registers.a_register
        self.registers.a_register = (self.registers.a_register - value) & 0xFF
