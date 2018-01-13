import unittest

from pybiogb.cpu.registers import Registers


class TestRegisters(unittest.TestCase):
    def test_bc_from_b_and_c(self):
        registers = Registers()
        registers.b_register = 0xFF
        registers.c_register = 0xFF
        self.assertEqual(registers.bc_register, 0xFFFF)

    def test_b_and_c_from_bc(self):
        registers = Registers()
        registers.bc_register = 0x1080
        self.assertEqual(registers.b_register, 0x10)
        self.assertEqual(registers.c_register, 0x80)

    def test_de_from_d_and_e(self):
        registers = Registers()
        registers.d_register = 0x20
        registers.e_register = 0xAB
        self.assertEqual(registers.de_register, 0x20AB)

    def test_d_and_e_from_de(self):
        registers = Registers()
        registers.de_register = 0x1080
        self.assertEqual(registers.d_register, 0x10)
        self.assertEqual(registers.e_register, 0x80)

    def test_hl_from_h_and_l(self):
        registers = Registers()
        registers.h_register = 0x20
        registers.l_register = 0xAB
        self.assertEqual(registers.hl_register, 0x20AB)

    def test_h_and_l_from_hl(self):
        registers = Registers()
        registers.hl_register = 0x1080
        self.assertEqual(registers.h_register, 0x10)
        self.assertEqual(registers.l_register, 0x80)

    def test_af_from_a_and_f(self):
        registers = Registers()
        registers.a_register = 0x20
        registers.f_register = 0xAB
        self.assertEqual(registers.af_register, 0x20AB)

    def test_a_and_f_from_af(self):
        registers = Registers()
        registers.af_register = 0x1080
        self.assertEqual(registers.a_register, 0x10)
        self.assertEqual(registers.f_register, 0x80)

    def test_z_flag(self):
        registers = Registers()
        registers.f_register = 0x80
        self.assertEqual(registers.z_flag, 1)
        registers.f_register = 0
        self.assertEqual(registers.z_flag, 0)

    def test_f_from_z_flag(self):
        registers = Registers()
        registers.z_flag = 1
        self.assertEqual(registers.f_register, 0x80)

    def test_n_flag(self):
        registers = Registers()
        registers.f_register = 0x40
        self.assertEqual(registers.n_flag, 1)
        registers.f_register = 0
        self.assertEqual(registers.n_flag, 0)

    def test_f_from_n_flag(self):
        registers = Registers()
        registers.n_flag = 1
        self.assertEqual(registers.f_register, 0x40)

    def test_h_flag(self):
        registers = Registers()
        registers.f_register = 0x20
        self.assertEqual(registers.h_flag, 1)
        registers.f_register = 0
        self.assertEqual(registers.h_flag, 0)

    def test_f_from_h_flag(self):
        registers = Registers()
        registers.h_flag = 1
        self.assertEqual(registers.f_register, 0x20)

    def test_c_flag(self):
        registers = Registers()
        registers.f_register = 0x10
        self.assertEqual(registers.c_flag, 1)
        registers.f_register = 0
        self.assertEqual(registers.c_flag, 0)

    def test_f_from_c_flag(self):
        registers = Registers()
        registers.c_flag = 1
        self.assertEqual(registers.f_register, 0x10)
