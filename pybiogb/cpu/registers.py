class Registers:
    def __init__(self):
        self.a_register = 0
        self.b_register = 0
        self.c_register = 0
        self.d_register = 0
        self.e_register = 0
        self.f_register = 0
        self.h_register = 0
        self.l_register = 0

        self.pc_register = 0
        self.sp_register = 0

    @property
    def bc_register(self):
        return (self.b_register << 8) | self.c_register

    @bc_register.setter
    def bc_register(self, value):
        self.b_register = (value >> 8) & 0xFF
        self.c_register = value & 0xFF

    @property
    def de_register(self):
        return (self.d_register << 8) | self.e_register

    @de_register.setter
    def de_register(self, value):
        self.d_register = (value >> 8) & 0xFF
        self.e_register = value & 0xFF

    @property
    def hl_register(self):
        return (self.h_register << 8) | self.l_register

    @hl_register.setter
    def hl_register(self, value):
        self.h_register = (value >> 8) & 0xFF
        self.l_register = value & 0xFF

    @property
    def af_register(self):
        return (self.a_register << 8) | self.f_register

    @af_register.setter
    def af_register(self, value):
        self.a_register = (value >> 8) & 0xFF
        self.f_register = value & 0xFF

    @property
    def z_flag(self):
        return 1 if self.f_register & 0x80 else 0

    @z_flag.setter
    def z_flag(self, value):
        if value:
            self.f_register |= 0x80
        else:
            self.f_register &= 0x7F

    @property
    def n_flag(self):
        return 1 if self.f_register & 0x40 else 0

    @n_flag.setter
    def n_flag(self, value):
        if value:
            self.f_register |= 0x40
        else:
            self.f_register &= 0xBF

    @property
    def h_flag(self):
        return 1 if self.f_register & 0x20 else 0

    @h_flag.setter
    def h_flag(self, value):
        if value:
            self.f_register |= 0x20
        else:
            self.f_register &= 0xDF

    @property
    def c_flag(self):
        return 1 if self.f_register & 0x10 else 0

    @c_flag.setter
    def c_flag(self, value):
        if value:
            self.f_register |= 0x10
        else:
            self.f_register &= 0xEF
