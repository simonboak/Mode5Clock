import time

rnum = 0xBAD

rows = [
	0x8F10, 0x9112, 0x9314, 0x9516, 0x18E9, 0x5899, 0x38D9, 0x78B9,
	0x9F20, 0xA122, 0xA324, 0xA526, 0x14E5, 0x5495, 0x34D5, 0x74B5,
	0xAF30, 0xB132, 0xB334, 0xB536, 0x1CED, 0x5C9D, 0x3CDD, 0x7CBD,
	0xBF40, 0xC142, 0xC344, 0xC546, 0x12E3, 0x5293, 0x32D3, 0x72B3,
  0x8F10, 0x9112, 0x9314, 0x9516, 0x18E9, 0x5899, 0x38D9, 0x78B9,
	0x9F20, 0xA122, 0xA324, 0xA526, 0x14E5, 0x5495, 0x34D5, 0x74B5,
	0xAF30, 0xB132, 0xB334, 0xB536, 0x1CED, 0x5C9D, 0x3CDD, 0x7CBD,
	0xBF40, 0xC142, 0xC344, 0xC546, 0x12E3, 0x5293, 0x32D3, 0x72B3
]

def get_random_bit():
  global rnum
  X = rnum
  lfsr_bit = ((X >> 0) ^ (X >> 1) ^ (X >> 3) ^ (X >> 12)) & 1
  rand_bit = (X | (X >> 2)) & 1
  rnum = (lfsr_bit << 15) | (rnum >> 1)
  return rand_bit

def next_cycle():
  for i, row in enumerate(rows):
    bit = get_random_bit()
    if i & 4:
      rows[i] = (bit << 15) | (rows[i] >> 1)
    else:
      rows[i] = (rows[i] << 1) | bit

def print_row(x):
  # 0 -> LED on, 1 -> LED off
  for i in range(15, -1, -1):
    if (x & (1 << i)):
      print('-', end='')
    else:
      print('0', end='')
  print()

def print_panel():
  # ANSI sequence to clear terminal
  print('\033[2J\033[1;1H')
  for row in rows:
    print_row(row)

if __name__ == '__main__':
  while True:
    next_cycle()
    print_panel()
    time.sleep(0.1)
