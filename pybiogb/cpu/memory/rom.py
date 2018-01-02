"""Module that manages ROM memory"""
import abc
import io
from collections import namedtuple


class Rom(metaclass=abc.ABCMeta):
    def __init__(self):
        self.rom_name = ''
        self.is_color = False
        self.mbc_type = 0
        self.rom_banks = 0
        self.ram_banks = 0

        self.content = []

    @staticmethod
    def get_rom_instance(file_name):
        """Returns an instance of the correct class depending on mbc type"""
        with open(file_name, 'rb') as file:
            file.seek(0x147)
            mbc_byte = int.from_bytes(file.read(1), 'little')
        instance = mbc_types[mbc_byte][1](mbc_byte)
        instance.load(file_name)
        return instance

    def load(self, file_name):
        with open(file_name, 'rb') as file:
            file.seek(0x134)
            self.rom_name = file.read(0xF).decode()

            file.seek(0x143)
            self.is_color = True if file.read(1) in [0x80, 0xC0] else False

            file.seek(0x147)
            mbc_byte = int.from_bytes(file.read(1), 'little')
            self.mbc_type = (mbc_byte, mbc_types[mbc_byte])

            rom_size_code = int.from_bytes(file.read(1), 'little')
            ram_size_code = int.from_bytes(file.read(1), 'little')
            self.rom_banks = self._get_rom_banks(file, rom_size_code)
            self.ram_banks = ram_sizes[ram_size_code].banks

            file.seek(0, io.SEEK_SET)
            for i in range(self.rom_banks):
                self.content.append(file.read(0x4000))

    @staticmethod
    def _get_rom_banks(file, rom_size_code):
        rom_size = rom_sizes.get(rom_size_code, None)
        if not rom_size:
            file.seek(0, io.SEEK_END)
            total = file.tell()
            return total / 0x4000
        else:
            return rom_size.banks

    @abc.abstractmethod
    def read(self, address):
        pass

    @abc.abstractmethod
    def write(self, address, value):
        pass


class MBC1(Rom):
    def __init__(self, banks):
        super().__init__()

    def read(self, address):
        pass

    def write(self, address, value):
        pass


mbc_types = {
    0: 'Rom Only',
    1: ('Rom + MBC1', MBC1),
    2: 'Rom + MBC1 + Ram',
    3: 'Rom + MBC1 + Ram + Battery',
    5: 'Rom + MBC2',
    6: 'Rom + MBC2 + Battery',
    8: 'Rom + Ram',
    9: 'Rom + Ram + Battery',
    0xB: 'Rom + MMMO1(Not working)',
    0xC: 'Rom + MMMO1 + SRam(Not working)',
    0xD: 'Rom + MMMO1 + SRam + Battery(Not working)',
    0xF: 'Rom + MBC3 + Timer + Battery(Timer not working)',
    0x10: 'Rom + MBC3 + Timer + Ram + Battery(Timer not working)',
    0x11: 'Rom + MBC3',
    0x12: 'Rom + MBC3 + Ram',
    0x13: 'Rom + MBC3 + Ram + Battery',
    0x15: 'Rom + MBC4',
    0x16: 'Rom + MBC4 + Ram',
    0x17: 'Rom + MBC4 + Ram + Battery',
    0x19: 'Rom + MBC5',
    0x1A: 'Rom + MBC5 + Ram',
    0x1B: 'Rom + MBC5 + Ram + Battery',
    0x1C: 'Rom + MBC5 + Rumble',
    0x1D: 'Rom + MBC5 + Rumble + SRam',
    0x1E: 'Rom + MBC5 + Rumble + SRam + Battery',
    0xFC: 'Pocket Cammera(Not working)',
    0xFD: 'Bandai TAMA5(Not working)',
    0xFE: 'Hudson HuC-3(Not working)',
    0xFF: 'Hudson HuC-1 + Ram + Battery'
}

Size = namedtuple('Size', 'bytes banks')

rom_sizes = {
    0: Size(16384 << 1, 2),
    1: Size(16384 << 2, 4),
    2: Size(16384 << 3, 8),
    3: Size(16384 << 4, 16),
    4: Size(16384 << 5, 32),
    5: Size(16384 << 6, 64),
    6: Size(16384 << 7, 128),
    7: Size(16384 << 8, 256),
    8: Size(16384 << 9, 512),
    0x52: Size(16384 * 72, 72),
    0x53: Size(16384 * 80, 80),
    0x54: Size(16384 * 96, 96)
}

ram_sizes = {
    0: Size(0, 0),
    1: Size(2048, 1),
    2: Size(8192, 1),
    3: Size(32768, 4),
    4: Size(131072, 16)
}
