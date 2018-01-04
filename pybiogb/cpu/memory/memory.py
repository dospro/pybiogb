from pybiogb.cpu.memory.rom import Rom


class Memory:
    def __init__(self):
        self.rom = None
        self.ram = None
        self.w_ram = None
        self.h_ram = None

    def load_gb_file(self, file_name):
        self.rom = Rom.get_rom_instance(file_name)
        self.ram = []
        for i in range(self.rom.ram_banks):
            self.ram.append([0] * 0x2000)

    def read_byte(self, address):
        if address < 0x8000:
            return self.rom.read(address)

    def write_byte(self, address, value):
        pass
