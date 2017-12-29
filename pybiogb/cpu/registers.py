class Registers:
    def __init__(self):
        self.z80_register_a = None
        self.z80_register_b = None
        self.z80_register_c = None
        self.z80_register_d = None
        self.z80_register_e = None
        self.z80_register_f = None
        self.z80_register_h = None
        self.z80_register_l = None

        self.z80_register_pc = None
        self.z80_register_sp = None

    @property
    def z80_register_bc(self):
        return (self.z80_register_b << 8) | self.z80_register_c

    @z80_register_bc.setter
    def z80_register_bc(self, value):
        self.z80_register_b = (value >> 8) & 0xFF
        self.z80_register_c = value & 0xFF

    @property
    def z80_register_de(self):
        return (self.z80_register_d << 8) | self.z80_register_e

    @z80_register_de.setter
    def z80_register_de(self, value):
        self.z80_register_d = (value >> 8) & 0xFF
        self.z80_register_e = value & 0xFF

    @property
    def z80_register_hl(self):
        return (self.z80_register_h << 8) | self.z80_register_l

    @z80_register_hl.setter
    def z80_register_hl(self, value):
        self.z80_register_h = (value >> 8) & 0xFF
        self.z80_register_l = value & 0xFF

    @property
    def z80_register_af(self):
        return (self.z80_register_a << 8) | self.z80_register_f

    @z80_register_af.setter
    def z80_register_af(self, value):
        self.z80_register_a = (value >> 8) & 0xFF
        self.z80_register_f = value & 0xFF