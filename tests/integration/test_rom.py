import os
import unittest

from pybiogb.cpu.memory.rom import Rom, MBC1


class TestRom(unittest.TestCase):
    def test_load_rom(self):
        rom = Rom.get_rom_instance('../roms/cpu_instrs/cpu_instrs.gb')
        print(os.path.dirname(os.path.realpath(__file__)))
        print(rom.rom_name)
        print(rom.mbc_type)
        self.assertEqual(rom.mbc_type[1].type_class, MBC1)
