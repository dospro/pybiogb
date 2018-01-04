"""Module that manages Ram memory"""
import abc


class Ram(metaclass=abc.ABCMeta):
    def __init__(self):
        self.ram_banks = 0

    @abc.abstractmethod
    def read(self, address):
        pass

    def write(self, address, value):
        pass
