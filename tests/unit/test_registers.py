import unittest

from pybiogb.cpu.registers import Registers


class TestRegisters(unittest.TestCase):
    def test_bc_from_b_and_c(self):
        registers = Registers()
        registers.z80_register_b = 0xFF
        registers.z80_register_c = 0xFF
        self.assertEqual(registers.z80_register_bc, 0xFFFF)

    def test_b_and_c_from_bc(self):
        registers = Registers()
        registers.z80_register_bc = 0x1080
        self.assertEqual(registers.z80_register_b, 0x10)
        self.assertEqual(registers.z80_register_c, 0x80)

    def test_de_from_d_and_e(self):
        registers = Registers()
        registers.z80_register_d = 0x20
        registers.z80_register_e = 0xAB
        self.assertEqual(registers.z80_register_de, 0x20AB)

    def test_d_and_e_from_de(self):
        registers = Registers()
        registers.z80_register_de = 0x1080
        self.assertEqual(registers.z80_register_d, 0x10)
        self.assertEqual(registers.z80_register_e, 0x80)

    def test_hl_from_h_and_l(self):
        registers = Registers()
        registers.z80_register_h = 0x20
        registers.z80_register_l = 0xAB
        self.assertEqual(registers.z80_register_hl, 0x20AB)

    def test_h_and_l_from_hl(self):
        registers = Registers()
        registers.z80_register_hl = 0x1080
        self.assertEqual(registers.z80_register_h, 0x10)
        self.assertEqual(registers.z80_register_l, 0x80)

    def test_af_from_a_and_f(self):
        registers = Registers()
        registers.z80_register_a = 0x20
        registers.z80_register_f = 0xAB
        self.assertEqual(registers.z80_register_af, 0x20AB)

    def test_a_and_f_from_af(self):
        registers = Registers()
        registers.z80_register_af = 0x1080
        self.assertEqual(registers.z80_register_a, 0x10)
        self.assertEqual(registers.z80_register_f, 0x80)

    def test_z_flag(self):
        registers = Registers()
        registers.z80_register_f = 0x80
        self.assertEqual(registers.z80_flag_z, 1)
        registers.z80_register_f = 0
        self.assertEqual(registers.z80_flag_z, 0)

    def test_f_from_z_flag(self):
        registers = Registers()
        registers.z80_flag_z = 1
        self.assertEqual(registers.z80_register_f, 0x80)

    def test_n_flag(self):
        registers = Registers()
        registers.z80_register_f = 0x40
        self.assertEqual(registers.z80_flag_n, 1)
        registers.z80_register_f = 0
        self.assertEqual(registers.z80_flag_n, 0)

    def test_f_from_n_flag(self):
        registers = Registers()
        registers.z80_flag_n = 1
        self.assertEqual(registers.z80_register_f, 0x40)

    def test_h_flag(self):
        registers = Registers()
        registers.z80_register_f = 0x20
        self.assertEqual(registers.z80_flag_h, 1)
        registers.z80_register_f = 0
        self.assertEqual(registers.z80_flag_h, 0)

    def test_f_from_h_flag(self):
        registers = Registers()
        registers.z80_flag_h = 1
        self.assertEqual(registers.z80_register_f, 0x20)

    def test_c_flag(self):
        registers = Registers()
        registers.z80_register_f = 0x10
        self.assertEqual(registers.z80_flag_c, 1)
        registers.z80_register_f = 0
        self.assertEqual(registers.z80_flag_c, 0)

    def test_f_from_c_flag(self):
        registers = Registers()
        registers.z80_flag_c = 1
        self.assertEqual(registers.z80_register_f, 0x10)
