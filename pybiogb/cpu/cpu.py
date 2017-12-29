"""Module that emulates gb-z80 cpu"""
from pybiogb.cpu.registers import Registers
from pybiogb.memory import Memory


class Cpu:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()

    def execute_opcode(self):
        pass
