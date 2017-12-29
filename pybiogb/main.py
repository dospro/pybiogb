from pybiogb.memory import Memory

gb = Memory()
header = gb.load_gb_file('blue.gb')
print(header)
