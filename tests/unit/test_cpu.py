import unittest
from collections import namedtuple

from pybiogb.cpu import cpu

Case = namedtuple('Case', 'a_before f_before value a_after f_after')


class TestAdc(unittest.TestCase):
    def test_cases(self):
        test_cpu = cpu.Cpu()
        for line in open('unit/mocks/adc_tests.json'):
            case = Case(*(int(i, 10) for i in line.split(' ')))
            test_cpu.registers.a_register = case.a_before
            test_cpu.registers.f_register = case.f_before
            test_cpu.adc(case.value)
            try:
                self.assertEqual(test_cpu.registers.a_register, case.a_after, 'a register is different')
                self.assertEqual(test_cpu.registers.f_register, case.f_after, 'flags are different')
            except AssertionError:
                raise


class TestAdd(unittest.TestCase):
    pass


class TestCpu(unittest.TestCase):
    def test_dec(self):
        test_cpu = cpu.Cpu()
        test_cpu.registers.a_register = 10
        test_cpu.opcodes[0x3D]()
        self.assertEqual(test_cpu.registers.a_register, 9)
