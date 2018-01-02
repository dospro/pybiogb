from pybiogb.cpu.memory.memory import Memory

gb = Memory()
header = gb.load_gb_file('blue.gb')
print(header)
