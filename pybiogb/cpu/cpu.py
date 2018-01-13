"""Module that emulates gb-z80 cpu"""
from pybiogb.cpu.registers import Registers
from pybiogb.cpu.memory.memory import Memory


class Cpu:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.opcodes = {
            0x3D: self.dec('a_register')
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

    def dec(self, register_name):
        def real_dec():
            s = self.registers.__dict__[register_name]
            self.registers.z_flag = s == 1
            self.registers.n_flag = True
            self.registers.h_flag = (s & 0xF) == 0
            self.registers.__dict__[register_name] = s - 1

        return real_dec
