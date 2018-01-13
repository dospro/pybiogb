"""Module that emulates gb-z80 cpu"""
from functools import partial

from pybiogb.cpu.registers import Registers
from pybiogb.cpu.memory.memory import Memory


class Cpu:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.opcodes = {
            0x3D: partial(self.dec, 'a_register')
        }

    def execute_opcode(self):
        pass

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
            self.push(self.registers.pc_register)
            self.registers.pc_register = address

    def dec(self, register_name):
        s = self.registers.__dict__[register_name]
        self.registers.z_flag = s == 1
        self.registers.n_flag = True
        self.registers.h_flag = (s & 0xF) == 0
        self.registers.__dict__[register_name] = s - 1
