"""Module that emulates gb-z80 cpu"""
from pybiogb.cpu.registers import Registers
from pybiogb.cpu.memory.memory import Memory


class Cpu:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.opcodes = {
            0x3D: DecOpcode(self.registers)
        }

    def execute_opcode(self):
        pass

    def adc(self, value):
        pass


class DecOpcode:
    def __init__(self, registers):
        self.registers = registers

    def __call__(self, *args, **kwargs):
        self.registers.z80_register_a -= 1
