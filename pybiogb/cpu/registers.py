class Registers:
    def __init__(self):
        self.z80_register_a = 0
        self.z80_register_b = 0
        self.z80_register_c = 0
        self.z80_register_d = 0
        self.z80_register_e = 0
        self.z80_register_f = 0
        self.z80_register_h = 0
        self.z80_register_l = 0

        self.z80_register_pc = 0
        self.z80_register_sp = 0

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

    @property
    def z80_flag_z(self):
        return 1 if self.z80_register_f & 0x80 else 0

    @z80_flag_z.setter
    def z80_flag_z(self, value):
        if value:
            self.z80_register_f |= 0x80

    @property
    def z80_flag_n(self):
        return 1 if self.z80_register_f & 0x40 else 0

    @z80_flag_n.setter
    def z80_flag_n(self, value):
        if value:
            self.z80_register_f |= 0x40

    @property
    def z80_flag_h(self):
        return 1 if self.z80_register_f & 0x20 else 0

    @z80_flag_h.setter
    def z80_flag_h(self, value):
        if value:
            self.z80_register_f |= 0x20

    @property
    def z80_flag_c(self):
        return 1 if self.z80_register_f & 0x10 else 0

    @z80_flag_c.setter
    def z80_flag_c(self, value):
        if value:
            self.z80_register_f = self.z80_register_f | 0x10
