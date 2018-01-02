import os
import unittest

from pybiogb.cpu.memory.rom import Rom


class TestRom(unittest.TestCase):
    def test_load_rom(self):
        rom = Rom.get_rom_instance('../roms/cpu_instrs/cpu_instrs.gb')
        print(os.path.dirname(os.path.realpath(__file__)))
        print(rom.rom_name)
        print(rom.mbc_type)
