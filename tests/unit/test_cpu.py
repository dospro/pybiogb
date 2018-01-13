import unittest

from pybiogb.cpu import cpu


class TestCpu(unittest.TestCase):
    def test_dec(self):
        test_cpu = cpu.Cpu()
        test_cpu.registers.a_register = 10
        test_cpu.opcodes[0x3D]()
        self.assertEqual(test_cpu.registers.a_register, 9)
